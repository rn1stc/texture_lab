%% Import Script for ODF Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
% CS = crystalSymmetry('D6', [1 1 1.633], 'mineral', 'Zr', 'color', 'light blue');
CS = loadCIF('/home/zhuk/cpfem/zr_AMS_DATA');
% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','intoPlane');
map = [ 1	1	1
        0.90909091	0.98181818	1
        0.818181819	0.963636362	1
        0.727272728	0.945454544	1
        0.636363637	0.927272726	1
        0.545454546	0.909090908	1
        0.454545455	0.89090909	1
        0.363636364	0.872727272	1
        0.272727273	0.854545454	1
        0.181818182	0.836363636	1
        0.090909091	0.818181818	1
        0	0.8	1 ];
%% Specify File Names

% path to files
dir_pat = 'zr_t5_16_1_33';
compare2 = '/home/zhuk/CLOUD/Crystal_Plasticity/Rolling/zr_rolling_mat/final/11266_FRF.TXT';
res = 5*degree;
if isfile(compare2)
    odf_comp = loadODF(compare2,CS,SS,'resolution',2.5*degree,...
        'interface','generic',...
        'ColumnNames', { 'phi1' 'phi2' 'Phi' 'Weight'}, 'Bunge',zvector);
    h = Miller(0,0,0,1,CS);
    plotPDF(odf_comp,h,'resolution',res,'halfwidth',res,...
        'contourf',1:1:6, 'nosymmetry','ShowText','on');
    caxis([0,6]);
    colormap(map);
    mtexColorbar;
    set(gcf, 'PaperUnits', 'inches');
    set(gcf, 'PaperSize', [3 2]);
    set(gca,'FontSize',18);
    set(gcf, 'Position',  [100, 100, 380, 380]);
    %break
    export_fig(['compare2.png'], '-painters');
    hold off
    close;
    e = [];
    comparing = true;
else
    comparing = false;
end
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
    ebsd_type = ["ebsd"]; %, "twinned_ebsd"]; %, "ebsd"];
    for j = 1:length(ebsd_type)
        work_dir = [pname '/' char(cur_dir) '/postProc/' char(ebsd_type(j))]; % postProc/
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
            psi = deLaValeePoussinKernel('halfwidth',2*degree);
            
            % create an EBSD variable containing the data
            ebsd = loadEBSD(fname,CS,...
                'ColumnNames', { 'x' 'y' 'z' 'Quat real' 'Quat i' 'Quat j' 'Quat k'}, 'Quaternion', 'Passive Rotation');
            %% Plot and save
            %rot = rotation('Euler',0*degree,170*degree,0*degree);
            %ebsd = rotate(ebsd,rot);
            
            odf = calcODF(ebsd.orientations,'resolution',2*degree,'halfwidth',4*degree);
            set(gcf, 'PaperUnits', 'inches');
            set(gcf, 'PaperSize', [4 2]);
            %% Plot and save
            h = Miller(0,0,0,1,CS);
            r = vector3d(1,1,0);
            
            pf = calcPoleFigure(odf,h,'resolution',1*degree);
            rot = rotation('axis',zvector,'angle',90*degree);
            pf = rotate(pf,rot);
            %plotPDF(odf,Miller({0,0,0,1}, CS),'resolution',1*degree,'contourf',0:0.5:6,'complete')
            plotPDF(ebsd.orientations,h,'resolution',6*degree,'halfwidth',6*degree,'contourf',1:1:6, 'nosymmetry','ShowText','on');
            
            caxis([0,6]);
            colormap(map);
            mtexColorbar;
            set(gcf, 'PaperUnits', 'inches');
            set(gcf, 'PaperSize', [3 2]);
            set(gca,'FontSize',18);
            set(gcf, 'Position',  [100, 100, 380, 380]);
            %break
            export_fig(['pf_' file.name '.png'], '-painters');
            hold off
            close;
            
            section = [fliplr(pf.intensities(270,:)) pf.intensities(90,:)];
            plot(linspace(-90, 90, length(section)), smooth(section),'LineWidth',2);
            xlim([-90 90]);
            xticks([-90 -60 -30 0 30 60 90]);
            set(gcf, 'PaperUnits', 'inches');
            set(gcf, 'PaperSize', [2.5 2]);
            set(gca,'FontSize',18);
            xlabel('Угол Ф, °');
            ylabel('Интен�?ивно�?ть');
            
            export_fig(['plot_' file.name '.png'], '-painters');
            hold off
            close;
            export(odf,[file.name '.odf'],'resolution',5*degree);
            % Calculating difference to reference odf
            if comparing == true
                e = [e calcError(odf, odf_comp)];
            end
            
            
        end
        if comparing == true
            plot(e);
            export_fig(['plot_e.png'], '-painters');
        end
        fprintf('Processed %s data in %s!\n', ebsd_type(j), cur_dir{1});
    end
end
cd (pname);
