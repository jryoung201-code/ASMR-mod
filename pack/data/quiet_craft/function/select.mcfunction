execute if score @s asmr matches 1..4 run function quiet_craft:change
execute if score @s asmr matches 6 at @s run function quiet_craft:custom
execute unless score @s asmr matches 1..4 unless score @s asmr matches 6 run tellraw @s {"text":"Quiet Craft — /trigger asmr set 1 (Rain), 2 (Campfire), 3 (Cave), 4 (Off), 6 (Custom track).","color":"gray"}
scoreboard players set @s asmr 0
