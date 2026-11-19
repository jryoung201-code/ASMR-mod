execute as @a[scores={asmr=..-1}] run function quiet_craft:select
execute as @a[scores={asmr=1..}] run function quiet_craft:select
scoreboard players enable @a asmr
scoreboard players remove @a[scores={qc_mode=1..3,qc_delay=1..}] qc_delay 1
execute as @a[scores={qc_mode=1..3,qc_delay=0}] at @s run function quiet_craft:play
