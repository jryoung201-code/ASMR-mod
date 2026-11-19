execute if score @s asmr matches 1..4 run function quiet_craft:change
execute if score @s asmr matches 6 at @s run function quiet_craft:custom
execute unless score @s asmr matches 1..4 unless score @s asmr matches 6 run function quiet_craft:menu
scoreboard players set @s asmr 0
