%% Import Script for PoleFigure Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('D6', [1 1 1.633], 'mineral', 'Zr', 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','intoPlane');

%% Specify File Names

% path to files
pname = '/home/zhuk/CLOUD/Crystal_Plasticity/twinning/dat_Jouk';
%pname = pwd

% which files to be imported
fname = {...
  [pname '/20364.dat_new'],...
  [pname '/10365.dat_new'],...
  [pname '/10366.dat_new'],...
  [pname '/10367.dat_new'],...
  };

%% Specify Miller Indice

h = { ...
  Miller(0,0,0,2,CS),...
  Miller(1,1,-2,0,CS),...
  Miller(1,0,-1,2,CS),...
  Miller(1,1,-2,2,CS),...
  };

%% Import the Data

% create a Pole Figure variable containing the data
pf = loadPoleFigure(fname,h,CS,SS,'interface','generic',...
  'ColumnNames', { 'Azimuth Angle' 'Polar Angle' 'Intensity'}, 'Columns', [1 2 3]);

%% Correct Data

%rot = rotation('Euler',0*degree,0*degree,0*degree);
%pf = rotate(pf,rot);
%pf = normalize(pf);


% plotting Pole Figure

%plot(pf,'contourf')
%plot(pf)
mtexColorbar

%export_VPSC(odfD1or.components{1}.center,'odfD1TEX.txt','weights',odfD1or.components{1}.weights);

%calculetion ODF
odf = calcODF(pf)
plot(odf,'contour','contourf')
mtexColorbar
set(gca,'CLim',[0 10],'XTick',(0:10:90),'XLim',[0 90],'YTick',(0:10:90),'YLim',[0 90])
grains = 512;
ori = calcOrientations(odf,grains)
odf1 = calcODF(ori)

%plotIPDF(odf,[zvector,yvector,xvector],'antipodal','contourf','colorrange',[0 5])
filename = 'zr_mono';

%% Writing EBSD to file
fileID = fopen([filename, '.material.config'],'w');
for i = 1:grains
    fprintf(fileID, '[Grain%03i]\ncrystallite 1\n(constituent)   phase 1   texture    %4i   fraction 1.0\n', i, i);
end
fprintf(fileID, '#-------------------#\n<texture>\n#-------------------#');
for i = 1:grains
    fprintf(fileID, '\n[Grain%03i]\n(gauss)   phi1 %7.3f   Phi %7.3f   phi2 %7.3f   scatter 0.0   fraction 1.0',...
        i, ori.phi1(i)*57.2958, ori.Phi(i)*57.2958, ori.phi2(i)*57.2958);
end
fclose(fileID);

%Plotting ODF section
%plot(odf1,'phi2',[45]*degree,'contour',0:0.5:15,'contourf')
%mtexColorbar

%pf_comp = calcPoleFigure(pf,odf1)
%plot(pf_comp,'contourf')
%mtexColorbar
%% Writing file with random one element per grain geometry

p = randperm(grains);
geomDim = 8;
fileGeom = fopen([filename, '_sim_ebsd.geom'],'w');
fprintf(fileGeom, '6	header\nGeometry generated with MATLAB script\ngrid	a %i	b %i	c %i', geomDim, geomDim, geomDim);
fprintf(fileGeom, '\nsize	x 1.0	y 1.0	z 1.0\norigin	x 0.0	y 0.0	z 0.0\nhomogenization	1\nmicrostructures	%i\n', grains);
k=1;
for i = 1:geomDim^2
    for j = 1:geomDim
        fprintf(fileGeom, '%5i ', p(k));
        k = k + 1;
    end
    fprintf(fileGeom, '\n');
end
fclose(fileGeom);