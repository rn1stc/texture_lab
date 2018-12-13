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
setMTEXpref('zAxisDirection','intoPlane');

%% Specify File Names

% path to files
dir_pat = 'zr_mono';
pname = pwd;
files0 = dir;
dir_loop = [];
directoryNames = {files0([files0.isdir]).name};
directoryNames = directoryNames(~ismember(directoryNames,{'.','..'}));
for i = [1:length(directoryNames)]
    if contains(directoryNames(i), dir_pat) == true
        dir_loop = [dir_loop directoryNames(i)];
    end
end
fprintf('Search pattern = %s\nFound ', dir_pat);
for i = [1:length(dir_loop)]
    fprintf('%s ', dir_loop{i});
end
fprintf('\n');
for i = [1:length(dir_loop)]
    cur_dir = dir_loop(i);
    ebsd_type = ["twinned_ebsd", "ebsd"];
    for j = 1:2
    work_dir = [pname '/' char(cur_dir) '/postProc/' char(ebsd_type(j))];
    if exist(work_dir,'dir') == 0
        fprintf('No valid %s data found in %s\n', ebsd_type(j), cur_dir{1});
        continue
    end
    cd (work_dir);
    files1 = dir('*.ebsd');
    for file = files1'
    % which files to be imported
    p1name = pwd;
    fname = [p1name '/' file.name];

    %% Import the Data

    % specify kernel
    psi = deLaValeePoussinKernel('halfwidth',5*degree);

    % create an EBSD variable containing the data
    ebsd = loadEBSD(fname,CS,...
      'ColumnNames', { 'x' 'y' 'z' 'phi1' 'Phi' 'phi2'}, 'Columns', [1 2 3 4 5 6], 'Bunge');
    %% Plot and save
    %rot = rotation('Euler',0*degree,170*degree,0*degree);
    %ebsd = rotate(ebsd,rot);

    odf = calcODF(ebsd.orientations);
    set(gcf, 'PaperUnits', 'inches');
    set(gcf, 'PaperSize', [4 2]);
    %% Plot and save
    h = Miller(0,0,0,2,CS);
    r = vector3d(1,1,0);
    pf = calcPoleFigure(odf,h,'resolution',5*degree,'complete');
    plotPDF(ebsd.orientations,h,'contourf',0:0.5:6);
    caxis([0,6]);
    set(gcf, 'PaperUnits', 'inches');
    set(gcf, 'PaperSize', [3 2]);
    set(gca,'FontSize',18);
    mtexColorMap summer;
    mtexColorbar;
    %break
    export_fig(['pf_' file.name '.png'], '-painters');
    hold off
    close;
    end
    fprintf('Processed %s data in %s!\n', ebsd_type(j), cur_dir{1});
    end
end
cd (pname);
