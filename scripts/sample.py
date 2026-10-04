from mcpi.minecraft import Minecraft
mc = Minecraft.create()

mc.postToChat("hogehoge")

pos = mc.player.getTilePos()
mc.setBlock(pos.x, pos.y+2, pos.z, 41)
