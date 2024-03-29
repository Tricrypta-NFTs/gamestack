#!bin/bash

p4 depot -o -t stream $1 > ./gamestack/p4d-generated-files/$1_depot.p4s 
p4 depot -i < ./gamestack/p4d-generated-files/$1_depot.p4s 
p4 stream -o -t mainline //$1/main > ./gamestack/p4d-generated-files/$1_mainline.p4s 
p4 stream -i < ./gamestack/p4d-generated-files/$1_mainline.p4s 

mkdir -p ./P4_Workspaces/$2_$1_main_c9
cp ./gamestack/p4d-files/.p4ignore ./P4_Workspaces/$2_$1_main_c9/.p4ignore

cd ./P4_Workspaces/$2_$1_main_c9
p4 client -o -S //$1/main $2_$1_main_c9 > ../../gamestack/p4d-generated-files/$1_client.p4s 
p4 client -i < ../../gamestack/p4d-generated-files/$1_client.p4s 

p4 set P4CLIENT=$2_$1_main_c9
p4 add .p4ignore
p4 submit -d "add .p4ignore for ue5"

cd ../.. && p4 client -d $2_$1_main_c9 && rm -rf P4_Workspaces

