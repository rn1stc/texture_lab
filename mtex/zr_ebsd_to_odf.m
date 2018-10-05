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
dir_pat = 'zr_random';
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
    work_dir = [pname '/' char(cur_dir) '/postProc/ebsd'];
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
    plot(odf,'phi1',0*degree,'contour',0:0.5:6,'contourf','silent');
    mtexColorbar;
    caxis([0,6]);

    %break
    saveas(gcf, [file.name '_odf.png']);
    close;
    end
    fprintf('%s processed!\n', cur_dir{1});
end
