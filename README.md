ArchoPlanet

Architectural project for urban visualisation and analysis based on:  
Blender - 3D modelling tool  
Openstreetmap.org - cartographic data  
NASA SRTM - topographic data  

How to use:  
1) Download and unpack the folder somewhere:  
https://github.com/snovvfall/ArchoPlanet/archive/master.zip  

2) Download and install Blender if you don't have it yet  
Official website is blender.org  

3) Launch ArchoPlanet.blend  

4) In the bottom half of the window you will see a text with parameters you can tweak  
It you want to use 'Srtm' or 'Osm and Srtm' mode you need to download
file with desired coordinates from here: http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/  

5) Hit "Run script" button located just above the parameters, usually near the center of the screen  
The process may require several minutes  

6) If you used 'Srtm' or 'Osm and Srtm' mode you will likely see big strange objects after the process finishes, remove them  
This problem will be fixed in the future  
If you are new to Blender, hover the mouse somewhere over top half of the window  
Press mouse wheel and move the mouse to rotate view  
Press mouse wheel and Shift to pan the view  
Press 'Z' keyboard button to see through all objects  
Press 'A' until orange color is gone to deselect all objects  
Press 'B', press left mouse button, move rectangle so it covers strange big objects and hit left mouse button again to select them  
Press Delete or 'X' to remove selected objects  

For developers:  
To run it in the console under Linux or MacOS X you may need to go to ArchoPlanet directory with 'cd' command and launch the main file,  
for example: cd /home/username/ArchoPlanet && blender ./ArchoPlanet.blend  