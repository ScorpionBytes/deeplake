import mmcv  # type: ignore
import logging
from mmcv import runner
from torch.utils.data import DataLoader

import time
import warnings
from typing import List, Tuple, Optional

from deeplake.constants import TIME_INTERVAL_FOR_CUDA_MEMORY_CLEANING
from .empty_memory import empty_cuda


@runner.RUNNERS.register_module()
class DeeplakeIterBasedRunner(runner.IterBasedRunner):
    def run(
        self,
        data_loaders: List[DataLoader],
        workflow: List[Tuple[str, int]],
        max_iters: Optional[int] = None,
        **kwargs,
    ) -> None:
        assert isinstance(data_loaders, list)
        assert mmcv.is_list_of(workflow, tuple)
        assert len(data_loaders) == len(workflow)
        if max_iters is not None:
            warnings.warn(
                "setting max_iters in run is deprecated, "
                "please set max_iters in runner_config",
                DeprecationWarning,
            )
            self._max_iters = max_iters
        assert (
            self._max_iters is not None
        ), "max_iters must be specified during instantiation"

        work_dir = self.work_dir if self.work_dir is not None else "NONE"
        self.logger.info(
            "Start running, host: %s, work_dir: %s",
            runner.utils.get_host_info(),
            work_dir,
        )
        self.logger.info(
            "Hooks will be executed in the following order:\n%s", self.get_hook_info()
        )
        self.logger.info("workflow: %s, max: %d iters", workflow, self._max_iters)
        self.call_hook("before_run")

        iter_loaders = [runner.IterLoader(x) for x in data_loaders]

        self.call_hook("before_epoch")

        formatter = logging.Formatter("%(relative)ss")
        start_time = time.time()

        while self.iter < self._max_iters:
            for i, flow in enumerate(workflow):
                self._inner_iter = 0
                mode, iters = flow
                if not isinstance(mode, str) or not hasattr(self, mode):
                    raise ValueError(
                        'runner has no method named "{}" to run a workflow'.format(mode)
                    )
                iter_runner = getattr(self, mode)
                for _ in range(iters):
                    if mode == "train" and self.iter >= self._max_iters:
                        break

                    iter_time = time.time()

                    if iter_time - start_time > TIME_INTERVAL_FOR_CUDA_MEMORY_CLEANING:
                        empty_cuda()
                        start_time = iter_time
                    iter_runner(iter_loaders[i], **kwargs)

        time.sleep(1)  # wait for some hooks like loggers to finish
        self.call_hook("after_epoch")
        self.call_hook("after_run")