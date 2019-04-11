  %% Import Script for ODF Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('D6', [1 1 1.633], 'mineral', 'Zr', 'color', 'light blue');
CS = crystalSymmetry('-43m');
CS = loadCIF('zr_AMS_DATA');
% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','intoPlane');

%% Specify File Names

% path to files
dir_pat = 'twin';
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
    ebsd_type = ["twinned_ebsd"]; %, "ebsd"];
    for j = 1:1
    work_dir = [pname '/' char(cur_dir) '/' char(ebsd_type(j))]; % postProc/
    if exist(work_dir,'dir') == 0
        fprintf('No valid %s data found in %s\n', ebsd_type(j), cur_dir{1});
        continue
    end
    cd (work_dir);
    files1 = dir('*.q');
    for file = files1'
    % which files to be imported
    p1name = pwd;
    fname = [p1name '/' file.name];

    %% Import the Data

    % specify kernel
    psi = deLaValeePoussinKernel('halfwidth',4*degree);

    % create an EBSD variable containing the data
    ebsd = loadEBSD(fname,CS,...
      'ColumnNames', { 'x' 'y' 'z' 'Quat real' 'Quat i' 'Quat j' 'Quat k'}, 'Quaternion', 'Passive Rotation');
    %% Plot and save
    %rot = rotation('Euler',0*degree,170*degree,0*degree);
    %ebsd = rotate(ebsd,rot);

    odf = calcODF(ebsd.orientations,'kernel',psi);
    figure
    hold on
    setMTEXpref('FontSize',18);
    plot(odf,'phi1',0*degree,'contour',0:0.5:6,'contourf','silent');
    caxis([0,6]);
    set(gcf, 'PaperUnits', 'inches');
    set(gcf, 'PaperSize', [3 2]);
    set(gca,'FontSize',18);
    mtexColorMap summer;
    mtexColorbar;
    %set(gcf, 'PaperPosition', [1 1 4 6]);    % can be bigger than screen 
    %set(gcf,'PaperPositionMode','auto');
    export_fig([file.name '_print_odf.png'], '-painters');
%     %break
%     %saveas(gcf, [file.name '_odf.png']);
    hold off;
    close;
    end
    fprintf('Processed %s data in %s!\n', ebsd_type(j), cur_dir{1});
    end
end
cd (pname);
