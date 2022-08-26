p4 set P4USER=$1
p4 set P4PORT=ssl:$2:1666
p4 trust -y

p4 typemap -i > /dev/null <<!
TypeMap:
                binary+w //depot/....exe
                binary+w //depot/....dll
                binary+w //depot/....lib
                binary+w //depot/....app
                binary+w //depot/....dylib
                binary+w //depot/....stub
                binary+w //depot/....ipa
                binary //depot/....bmp
                text //depot/....ini
                text //depot/....config
                text //depot/....cpp
                text //depot/....h
                text //depot/....c
                text //depot/....cs
                text //depot/....m
                text //depot/....mm
                text //depot/....py
                binary+l //depot/....uasset
                binary+l //depot/....umap
                binary+l //depot/....upk
                binary+l //depot/....udk
                binary+l //depot/....ubulk
!

p4 depot -d depot