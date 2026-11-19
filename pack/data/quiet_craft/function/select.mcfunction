execute if score @s asmr matches 1..4 run function quiet_craft:change
execute unless score @s asmr matches 1..4 run tellraw @s {"text":"Quiet Craft — /trigger asmr set 1 (Rain), 2 (Campfire), 3 (Cave), 4 (Off).","color":"gray"}
scoreboard players set @s asmr 0
