import os.path
import tempfile

from datatig.writers.frictionless.frictionless import FrictionlessWriter
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeDatatigFrictionless(BasePipe):

    def __init__(self, output_dir="/", output_filename="frictionless.zip"):
        self.output_dir = output_dir
        self.output_filename = output_filename

    def start_build(self, current_info: CurrentInfo) -> None:

        temp_dir = tempfile.mkdtemp()
        temp_out_filename = os.path.join(temp_dir, "frictionless.zip")

        frictionless_writer = FrictionlessWriter(
            current_info.get_context("datatig")["config"],
            current_info.get_context("datatig")["datastore"],
            temp_out_filename,
        )
        frictionless_writer.go()

        with open(temp_out_filename, "rb") as fp:
            self.build_directory.write(self.output_dir, self.output_filename, fp.read())
