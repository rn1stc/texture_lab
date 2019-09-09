function [ ] = PENETRATION_DEPTH ( )
close all
global tabule pom pom2; %pom=choice of type of measuring, pom2=choice of type of attenuation coefficient
pom = 'BB'; % default value
pom2 = 'linear'; % default value
tabule = figure(1);
set(tabule,'units','characters','Position',[20 10 176 44],'Color',[1 1 0.9]);
nadpis= uicontrol('Style','text','units','normalized','pos',[0.01 0.89 0.82 0.09],'FontSize',30,'FontWeight','bold','FontAngle','italic','BackgroundColor',[0.6 1 0.6],'ForegroundColor',[0.5 0 0.9],'HandleVisibility','on','String','GRAPHS OF PENETRATION DEPTH'); 
attention = uicontrol('Style','text','units','normalized','pos',[0.01 0.89 0.82 0.09],'FontSize',20,'FontWeight','bold','FontAngle','italic','BackgroundColor',[0 0 1],'ForegroundColor',[1 1 0],'visible','off','String','ATTENTION');
vyber = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'on', 'Title','Type of result','units','normalized','Position', [0.016 0.53 0.29 0.292],'SelectionChangeFcn',@vyber_fc,'Tag','typeofresult');
vyber_BB = uicontrol('Style','Radio','units','normalized','pos',[0.05 0.77 0.9 0.17],'FontSize',12,'BackgroundColor',[0 1 1],'parent',vyber,'HandleVisibility','on','Tag','BB','String','Bragg-Brentano');
vyber_GID = uicontrol('Style','Radio','units','normalized','pos',[0.05 0.55 0.9 0.17],'FontSize',12,'BackgroundColor',[0 1 1],'parent',vyber,'HandleVisibility','on','Tag','GID','String','grazing incidence');
vyber_RS = uicontrol('Style','Radio','units','normalized','pos',[0.05 0.33 0.9 0.17],'FontSize',12,'BackgroundColor',[0 1 1],'parent',vyber,'HandleVisibility','on','Tag','RS','String','stress');
vyber_omega = uicontrol('Style','Radio','units','normalized','pos',[0.05 0.11 0.9 0.17],'FontSize',12,'BackgroundColor',[0 1 1],'parent',vyber,'HandleVisibility','on','Tag','omega','String','omega-scan');
set(vyber,'selectedobject',vyber_BB);
 function vyber_fc(~,eventdata)
 type = get(eventdata.NewValue,'Tag') ;
 main_enable(type);
 set(vyber,'Tag',get(eventdata.NewValue,'Tag'));
 end
 function main_enable(type)
 set(values, 'visible','on'); % visible or invisible parts of program
 set(limits, 'visible','on');
 set(angle, 'visible','on');
 set(Tvalue, 'visible','on');
 switch type
 case {'BB', 'GID'}
 set(values, 'visible','off');
 end
 switch type
 case 'omega'
 set(limits, 'visible','off');
 end
 switch type
 case {'BB', 'RS', 'omega'}
 set(angle, 'visible','off');
 end
 switch type
 case 'RS'
 set(Tvalue, 'visible','off');
 end
 switch type %modification of global parameter "pom"=choice of type of measuring
 case 'BB'
 pom = 'BB'; % Bragg-Brentano
 case 'GID'
 pom = 'GID'; % grazing incidence diffraction
 case 'RS'
 pom = 'RS'; % measuring of residual stresses
 case 'omega'
 pom = 'omega'; % for omega-scan
 end
 end

values = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'off', 'Title','Values of sin2psi','units','normalized','Position', [0.67 0.47 0.29 0.354]);
values_min = uicontrol('Style','text','units','normalized','pos',[0.065 0.8 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',values,'String','sin2psi_min');
values_max = uicontrol('Style','text','units','normalized','pos',[0.065 0.5 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',values,'String','sin2psi_max');
values_del = uicontrol('Style','text','units','normalized','pos',[0.065 0.2 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',values,'String','delta sin2psi');
values_min_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.8 0.275 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',values,'String','0');
values_max_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.5 0.275 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',values,'String','0.8');
values_del_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.2 0.275 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',values,'String','0.1');
limits = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'on', 'Title','Limits of measuring','units','normalized','Position', [0.357 0.603 0.29 0.218]);
limits_min = uicontrol('Style','text','units','normalized','pos',[0.08 0.60 0.49 0.24],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',limits,'String','2theta_min, deg');
limits_max = uicontrol('Style','text','units','normalized','pos',[0.08 0.25 0.49 0.24],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',limits,'String','2theta_max, deg');
limits_min_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.60 0.35 0.24],'FontSize',12,'BackgroundColor',[1 1 1],'parent',limits,'String','147');
limits_max_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.25 0.35 0.24],'FontSize',12,'BackgroundColor',[1 1 1],'parent',limits,'String','165');
angle = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'off', 'Title','Incident angle','units','normalized','Position', [0.396 0.417 0.245 0.137]);
angle_m = uicontrol('Style','text','units','normalized','pos',[0.08 0.3 0.4 0.45],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',angle,'String','alpha, deg');
angle_m_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.3 0.35 0.45],'FontSize',12,'BackgroundColor',[1 1 1],'parent',angle,'String','1.5');
Tvalue = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'on', 'Title','Value of penetration depth','units','normalized','Position', [0.016 0.03 0.316 0.229]);
Tvalue_theta = uicontrol('Style','text','units','normalized','pos',[0.08 0.65 0.34 0.24],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',Tvalue,'String','2theta, deg');
TvalueT = uicontrol('Style','text','units','normalized','pos',[0.08 0.25 0.34 0.24],'FontSize',12,'BackgroundColor',[0.7 0.8 1],'parent',Tvalue,'String','T^ef, mum');
Tvalue_theta_edit = uicontrol('Style','edit','units','normalized','pos',[0.5 0.65 0.42 0.24],'FontSize',12,'BackgroundColor',[1 1 1],'parent',Tvalue,'String','156');
TvalueT_edit = uicontrol('Style','edit','units','normalized','pos',[0.5 0.25 0.42 0.24],'FontSize',12,'Enable','off','parent',Tvalue);
Aten_vyber = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'on', 'Title','Type of attenuation coefficient','units','normalized','Position', [0.016 0.3 0.36 0.2],'SelectionChangeFcn',@Aten_vyber_fc,'Tag','typeofattencoef');
Aten_vyber_linear = uicontrol('Style','Radio','units','normalized','pos',[0.08 0.6 0.76 0.27],'FontSize',12,'BackgroundColor',[0 1 1],'parent',Aten_vyber,'HandleVisibility','on','Tag','linear','String','linear attenuation coefficient');
Aten_vyber_mass = uicontrol('Style','Radio','units','normalized','pos',[0.08 0.2 0.76 0.27],'FontSize',12,'BackgroundColor',[0 1 1],'parent',Aten_vyber,'HandleVisibility','on','Tag','mass','String','mass attenuation coefficient');
set(Aten_vyber,'selectedobject',Aten_vyber_linear);
 function Aten_vyber_fc(~,eventdata)
 type = get(eventdata.NewValue,'Tag') ;
 atten_enable(type);
 set(Aten_vyber,'Tag',get(eventdata.NewValue,'Tag'));
 end
 function atten_enable(type)
 set(atten_lin_edit, 'enable','on','String','890'); % default values for attenuation coefficients (for alpha-Fe)
 set(atten_mass_edit, 'enable','on','String','113.23');
 set(atten_density_edit, 'enable','on','String','7.86');
 switch type % enable or not fill edits by values
 case 'linear'
 set(atten_mass_edit, 'enable','off','String','');
 set(atten_density_edit, 'enable','off','String','');
 end
 switch type % enable or not fill edits by values
 case 'mass'
 set(atten_lin_edit, 'enable','off','String','');
 end
 %%%%%%%%%%%%%%%%%%%%%%%%%%
 switch type %modification of global parameter "pom2"==choice of type of attenuation coefficient
 case 'linear'
 pom2 = 'linear';
 case 'mass'
 pom2 = 'mass';
 end
 end
atten = uibuttongroup('FontSize',15,'FontWeight','bold','BackgroundColor',[0 1 1],'visible', 'on', 'Title','Values of attenuation coefficient','units','normalized','Position', [0.396 0.03 0.377 0.354]);
atten_lin = uicontrol('Style','text','units','normalized','pos',[0.09 0.70 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',atten,'String','mu, 1/cm');
atten_mass = uicontrol('Style','text','units','normalized','pos',[0.09 0.45 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',atten,'String','mu/rho, cm^2/g');
atten_density = uicontrol('Style','text','units','normalized','pos',[0.09 0.20 0.45 0.13],'FontSize',12,'BackgroundColor',[1 0.9 0.75],'parent',atten,'String','rho, g/cm^3');
atten_lin_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.70 0.3 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',atten,'String','890');
atten_mass_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.45 0.3 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',atten,'String','113.23','enable','off','String','');
atten_density_edit = uicontrol('Style','edit','units','normalized','pos',[0.6 0.20 0.3 0.13],'FontSize',12,'BackgroundColor',[1 1 1],'parent',atten,'String','7.86','enable','off','String','');
execute = uicontrol('Style','pushbutton','String','EXECUTE','units','normalized','pos',[0.78 0.03 0.18 0.38],'FontSize',23,'BackgroundColor',[1 0 0],'ForegroundColor',[1 1 0],'FontWeight','bold','FontAngle','oblique','CallBack',@execute_fc);
 function execute_fc(~,~)
 x1 = str2double(get(limits_min_edit,'String')); % reading variables
 x2 = str2double(get(limits_max_edit,'String'));
 hodnota = str2double(get(Tvalue_theta_edit,'String'));
 alpha = str2double(get(angle_m_edit,'String'));
 sinmin = str2double(get(values_min_edit,'String'));
 sinmax = str2double(get(values_max_edit,'String'));
 deltasin = str2double(get(values_del_edit,'String'));

 sinmin2=abs(sinmin);
 sinmax2=abs(sinmax);

 if (x1<0 | x2>180 | x1>x2 | x1/0~=inf | x2/0~=inf) & strcmp(pom,'omega')==0
%warning if is a wrong entered value
 set(attention,'visible','on','String','Check values of "Limits of measuring"');
 return
 elseif (hodnota>x2 | hodnota<x1 | hodnota/0~=inf) & strcmp(pom,'RS')==0
 set(attention,'visible','on','String','Check value of "Value of penetration depth"');
 return
 elseif (alpha<0 | alpha/0~=inf) & strcmp(pom,'GID')==1
 set(attention,'visible','on','String','Check value of "Incident angle"');
 return
 elseif (sinmin2>sinmax2|sinmax2>1|sinmax2-sinmin2>=0.9|deltasin<=0|deltasin>=1|(sinmin2+1)/0~=inf|sinmax2/0~=inf|deltasin/0~=inf) & (strcmp(pom,'RS')==1 | strcmp(pom,'omega')==1)
 set(attention,'visible','on','String','Check value of "Values of sin2psi"');
 return
 end
 switch pom2 %reading variable parameter "pom2"==choice of type of attenuation coefficient
 case 'linear'
 my = str2double(get(atten_lin_edit,'String'));
 case 'mass'
 my = str2double(get(atten_mass_edit,'String'))*str2double(get(atten_density_edit,'String'));
 end

 if my<=0 | my/0~=inf %warning if is a wrong entered value
 set(attention,'visible','on','String','Check values of "Values of attenuation coefficient"');
 return
 end
 
 set(attention,'visible','off');

 switch pom %call the relevant function for calculation of the value of penetration depth
 case 'BB' % Bragg-Brentano geometry
 T = hloubka(0,my,x1,x2,hodnota,0);
 set(TvalueT_edit,'String',num2str(T));
 case 'GID' % grazing incidence diffraction
 T = hloubka(1,my,x1,x2,hodnota,alpha);
 set(TvalueT_edit,'String',num2str(T));
 case 'RS' % measuring of residual stresses
 nap_hloubka(x1,x2,sinmin,sinmax,deltasin,my)
 case 'omega' % for omega-scan
 T_sinpsi(hodnota,my,sinmin,sinmax,deltasin)
 end

 end % fce(execute)
end % fce (penetration_depth)
%%
function T = hloubka(geometrie,my,x1,x2,hodnota,alfa)
figure(2); % new figure

 if geometrie==0 % Bragg-Brentano geometry

 colordef white
 colormap('default')

 x = x1:0.01:x2; % values of axes "x"
 radx = (pi*x)/360; %" axes x" (degrees to radians)
 hod = (pi*hodnota)/360; % "axes y" (degrees to radians)
 y=(10000*sin(radx))/(2*my); % function
 plot(x,y,'b-','LineWidth',2)
 set(gca,'LineWidth',2,'FontWeight','bold','FontSize',15)
 grid
 T=(10000*sin(hod))/(2*my) % write value of penetration depth for one value of angle
 xlabel('2\theta[°]')
 ylabel('T[\mum]')

 elseif geometrie==1 % grazing incidence diffraction
 x = x1:0.01:x2; % values of axes "x"
 radx = (pi*x)/360;%" axes x" (degrees to radians)
 rada = (pi*alfa)/180; % incidence angle (degrees to radians)
 hod = (pi*hodnota)/360;% "axes y" (degrees to radians)
 T=(10000*sin(rada)*sin(2*hod-rada))/(my*(sin(rada)+sin(2*hod-rada)))% write value of penetration depth for one value of angle
 y=(10000*sin(rada)*sin(2*radx-rada))./(my*(sin(rada)+sin(2*radx-rada))); 
 
 aprox=10000*sin(rada)/my; % approximation function for small incidence angles
 hold on;
 plot(x,y,'b-','LineWidth',2)
 plot(x,aprox,'r--','LineWidth',2)
 set(gca,'LineWidth',2,'FontWeight','bold','FontSize',15)
 grid
 xlabel('2\theta[°]')
 ylabel('T[\mum]')
 hold off;
 
 end
end% Bragg-Brentano geometry & grazing incidence diffraction

function nap_hloubka(x1,x2,sinmin,sinmax,deltasin,my) 
close all;
sinmin2=abs(sinmin);
sinmax2=abs(sinmax);
 x = x1:0.01:x2;% values of axes "x"
 radx = (pi*x)/180;%" axes x" (degrees to radians)
 D = [sinmin2:deltasin:sinmax2];% values of a step of value sin^2psi

 pocet = length(D); % number of a step of value sin^2psi

 colordef white
 colormap('default')

 for i = 1:pocet

 subplot(3,3,i) % net of graphs
 y=10000*(sin(radx/2).^2-D(i))./(2*my*sin(radx/2)*sqrt(1-D(i))); 

 plot(x,y,'b-','LineWidth',2);
 set(gca,'LineWidth',2,'FontWeight','bold','FontSize',15)

 title(['Sin^2\psi = ',num2str(D(i))])
 grid
 axis normal
 xlabel('2\theta[°]')
 ylabel('T_e_f[\mum]')
 xlim([x1 x2])
 end
end% measuring of residual stresses
function T_sinpsi(dvetheta,my,sinmin,sinmax,delta)
close all;

sinmin2=abs(sinmin);
sinmax2=abs(sinmax);

 radtheta = (pi*dvetheta)/360; % diffraction angle (degrees to radians)
 x=sinmin:delta:sinmax; %" axes x" (degrees to radians)-interval of sin^2psi

 y=10000*(sin(radtheta).^2-x)./(2*my*sin(radtheta)*sqrt(1-x));

 plot(x,y,'ro--','LineWidth',2);
 set(gca,'LineWidth',2,'FontWeight','bold','FontSize',15)
 grid
 xlabel('sin^2\psi')
 ylabel('T[\mum]')
 title(['2\theta = ',num2str(dvetheta),'°'])
end % for omega-scan