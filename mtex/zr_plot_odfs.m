%% Import Script for ODF Data
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
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = pwd;

files = dir('11183.TXT.linearODF');
for file = files'
% which files to be imported
fname = [pname '\' file.name];

%% Import the Data

% specify kernel
psi = deLaValeePoussinKernel('halfwidth',5*degree);

% create an EBSD variable containing the data
odf = loadODF(fname,CS,'resolution',5*degree,...
  'ColumnNames', { 'phi1' 'Phi' 'phi2' 'weights'}, 'Bunge');
%% Plot and save
%h = Miller(0,0,0,1,CS);
%pf = calcPoleFigure(odf,h,'resolution',5*degree,'complete');
%plot(pf,'contourf');
%plotDiff(pf,pf2)
mtexColorbar;
plot(odf,'phi1',0*degree,'contour',0:0.5:6,'contourf','silent');
colorbar;
caxis([0,6]);
hFig = figure(1);
set(hFig, 'Position', [10 10 800 700]);
%break
saveas(gcf, [file.name '_odf.png']);
end
