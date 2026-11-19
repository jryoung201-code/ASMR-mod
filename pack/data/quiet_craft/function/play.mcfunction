execute if score @s qc_mode matches 1 run playsound minecraft:weather.rain ambient @s ~ ~1.5 ~ 0.18 1 0.06
execute if score @s qc_mode matches 2 run playsound minecraft:block.campfire.crackle ambient @s ~ ~1.5 ~ 0.24 0.9 0.08
execute if score @s qc_mode matches 3 run playsound minecraft:block.pointed_dripstone.drip_water ambient @s ~ ~1.5 ~ 0.28 0.8 0.08
execute if score @s qc_mode matches 1 store result score @s qc_delay run random value 28..46
execute if score @s qc_mode matches 2 store result score @s qc_delay run random value 55..95
execute if score @s qc_mode matches 3 store result score @s qc_delay run random value 24..72
