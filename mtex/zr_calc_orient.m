%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('D6', [1 1 1.633], 'mineral', 'Zr', 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('1');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify grid dimensions

geomDim = 32;
grains = geomDim^3;
Ndisc = grains;

%% Specify File Names

% path to files
pname = pwd;

files = dir('11183.TXT');
for file = files'
% which files to be imported
fname = [pname '/' file.name];
% create an EBSD variable containing the data
odf = loadODF(fname,CS,'resolution',5*degree,...
  'ColumnNames', { 'phi1' 'phi2' 'Phi' 'weights'}, 'Bunge',zvector);
p = odf.components{2,1}.weights;
for i = 1:length(p)
    if p(i) < 0
        p(i) = 0;
    end
        
end
p=p./sum(p);
odf.components{2,1}.weights = p;
odf0 = 0.5*uniformODF(CS) + 0.5*fibreODF(Miller(0,0,0,1,CS),zvector);
plot(odf,'phi1',0*degree,'contour',0:0.5:6,'contourf','silent');
colorbar;
caxis([0,6]);
hFig = figure(1);
set(hFig, 'Position', [10 10 800 700]);
%break
saveas(gcf, [file.name '_odf_abs.png']);
ori = discreteSample(odf, Ndisc);
psi = calcKernel(ori);
odf2 = calcODF(ori,'kernel',psi);
plot(odf2,'phi1',0*degree,'contour',0:0.5:6,'contourf','silent');
colorbar;
caxis([0,6]);
hFig = figure(1);
set(hFig, 'Position', [10 10 800 700]);
%break
saveas(gcf, [file.name '_odf_simulated.png']);

%% Writing EBSD to file
fileID = fopen([file.name '_sim_ebsd.config'],'w');
fprintf(fileID, '#Sample orientations generated with MTEX for file %s \n#-------------------#\n<microstructure>\n#-------------------#\n', file.name);
for i = 1:Ndisc
    fprintf(fileID, '[Grain%04i]\ncrystallite 1\n(constituent)   phase 1   texture    %4i   fraction 1.0\n', i, i);
end
fprintf(fileID, '#-------------------#\n<texture>\n#-------------------#');
for i = 1:Ndisc
    fprintf(fileID, '\n[Grain%05i]\n(gauss)   phi1 %7.3f   Phi %7.3f   phi2 %7.3f   scatter 0.0   fraction 1.0',...
        i, ori.phi1(i)*57.2958, ori.Phi(i)*57.2958, ori.phi2(i)*57.2958);
end
fclose(fileID);

%% Writing file with random one element per grain geometry

p = randperm(grains);
fileGeom = fopen([file.name '_sim_ebsd.geom'],'w');
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
end
        
    
