scoreboard players operation @s qc_mode = @s asmr
stopsound @s ambient quiet_craft:custom
scoreboard players set @s qc_delay 0
execute if score @s qc_mode matches 1 run tellraw @s {"text":"Quiet Craft: Rain","color":"aqua"}
execute if score @s qc_mode matches 2 run tellraw @s {"text":"Quiet Craft: Campfire","color":"gold"}
execute if score @s qc_mode matches 3 run tellraw @s {"text":"Quiet Craft: Cave","color":"gray"}
execute if score @s qc_mode matches 4 run tellraw @s {"text":"Quiet Craft: Off","color":"gray"}
