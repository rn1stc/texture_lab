%% Import Script for PoleFigure Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('m-3m', [3.65 3.65 3.65], 'mineral', 'Iron-gamma', 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = 'D:\texture\pyth\';
%pname = pwd

% which files to be imported
fname = {...
  [pname '/12018odf.dat'],...
  [pname '/12019odf.dat'],...
  [pname '/12017odf.dat'],...
  };

%% Specify Miller Indice

h = { ...
  Miller(2,0,0,CS),...
  Miller(0,2,2,CS),...
  Miller(1,1,1,CS),...
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
%mtexColorbar

%export_VPSC(odfD1or.components{1}.center,'odfD1TEX.txt','weights',odfD1or.components{1}.weights);

%calculetion ODF
odf = calcODF(pf)
%plot(odf,'phi2',[45]*degree,'contour','contourf')
mtexColorbar
set(gca,'CLim',[0 10],'XTick',(0:10:90),'XLim',[0 90],'YTick',(0:10:90),'YLim',[0 90])
ori = calcOrientations(odf,500)
odf1 = calcODF(ori)

plotIPDF(odf,[zvector,yvector,xvector],'antipodal','contourf','colorrange',[0 5])


%% Writing EBSD to file
fileID = fopen('EP450DUO_00.txt','w');
for i = 1:500
    fprintf(fileID, '[Grain%03i]\ncrystallite 1\n(constituent)   phase 1   texture    %4i   fraction 1.0\n', i, i);
end
fprintf(fileID, '#-------------------#\n<texture>\n#-------------------#');
for i = 1:500
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