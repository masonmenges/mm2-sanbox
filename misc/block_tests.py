from prefect.blocks.core import Block
from prefect.testing.utilities import prefect_test_harness

with prefect_test_harness():
    class MyBlock(Block):
        setting_1: str = "foo"

    blk1 = MyBlock(setting_1 = "bar")
    blk1.save("a-block")
    print(blk1._to_block_schema())
   

    # redefining the block with a new schema
    class MyBlock(Block):
        setting_2: float = 1

    MyBlock.model_config["extra"] = "forbid"

    blk2 = MyBlock(setting_2=0.5)
    blk2.model_config["extra"] = "forbid"
    blk2.save("a-block", overwrite=True)

    blk3 = MyBlock.load("a-block")
    print(blk3._to_block_schema())
    print(blk3.model_dump_json())
    print(blk3.setting_1) # old data still accessible
    print(blk3.setting_2)