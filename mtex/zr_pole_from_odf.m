%% Import Script for ODF Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('D6', [1 1 1.633], 'mineral', 'Zr', 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('D6');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = '/home/zhuk/cpfem/zr_roll/postProc/odf/';

files = dir('*.linodf');
for file = files'
% which files to be imported
fname = [pname file.name];

%% Import the Data

% specify kernel
psi = deLaValeePoussinKernel('halfwidth',10*degree);

% create an EBSD variable containing the data
odf = loadODF(fname,CS,SS,'density','kernel',psi,'resolution',5*degree,...
  'interface','generic',...
  'ColumnNames', { 'phi1' 'Phi' 'phi2' 'intencity'}, 'Bunge');
%% Plot and save
h = Miller(1,0,-1,1,CS);
r = vector3d(1,1,0);
pf = calcPoleFigure(odf,h,'resolution',5*degree,'complete');
plotPDF(pf,h);
%plot(odf,'phi1',[0 30 60 90]*degree,'contourf','silent');
colorbar;
%caxis([0,3]);
%hFig = figure(1);
%set(hFig, 'Position', [10 10 700 800]);
break
saveas(gcf, [file.name '_odf.png']);
end
