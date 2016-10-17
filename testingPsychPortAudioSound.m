% Sound Variables
Duration=0.5;
Fs=10000;   % Sample rate in Hz
FadeTime=50;   %Duration of fade function (ms)
st=(0:1/Fs:Duration)'; %
nrchannels = 1; % One channel only -> Mono sound.
repetitions = 0;
tone = MakeBeep(500,0.1);% extemes mark tone

% Keys
KbName('UnifyKeyNames');
rightKey = KbName('d'); %KbName('4');
leftKey = KbName('a');%KbName('6');
returnKey = KbName('f');
NextKey = kbName('s');

% Perform basic initialization of the sound driver:
InitializePsychSound;
% Open the default audio device [], with default mode [] (==Only playback),
% and a required latencyclass of zero 0 == no low-latency mode, as well as
% a frequency of Fs and nrchannels sound channels.
% This returns a handle to the audio device:
pahandle = PsychPortAudio('Open', [], [], 0, Fs, nrchannels);
% inital sound vs
ToneFreq(1,:)=[440 459.48 479.82 501.07 523.25 546.41 570.61 595.87 622.25 649.80 678.57 708.61 739.99 772.75 806.96 842.69 880];
ToneFreq(2,:)=[0.4	0.391 0.383 0.375 0.367 0.359 0.351 0.344 0.336 0.329 0.322 0.315 0.309 0.302 0.295 0.289 0.283];

% set levels and corrected matrix Freq-Level
index=1;
InitialLevel=0.45;

PossibleFMs = 3:0.5:9;    

Rndm_start_param = randperm(length(PossibleFMs));

InitialFM_start = PossibleFMs(Rndm_start_param(1));
InitialFM = InitialFM_start;
First_InitialFM = InitialFM;
A = InitialLevel*ones(size(st,1),1);

% Get the faded signal
A(1:Fs*FadeTime/1000)=FadeInFct.*A(1:Fs*FadeTime/1000);
A((size(st,1)-Fs*FadeTime/1000):size(st,1))=FadeOutFct.*A((size(st,1)-Fs*FadeTime/1000):size(st,1));

son=A.*sin(2*pi*ToneFreq(1,index)*st).*sin(2*pi*InitialFM*st);

current_row = Random_list(current_trial);
    
 Not_done = 1;
        while Not_done == 1;
            
    PsychPortAudio('FillBuffer', pahandle, son');
    PsychPortAudio('Start', pahandle, repetitions, 0, 1);
    Start_sound = GetSecs;
    % Animationloop:
    Not_done2 = 1;
    no_press =1;

    while Not_done2 == 1;


                        % CHANGE FREQUENCY
        if no_press == 1;

            [ keyIsDown, seconds, keyCode ] = KbCheck; %#ok<ASGLU>

            if keyIsDown
                if keyCode(rightKey)
                    if InitialFM<19
                        InitialFM=InitialFM+0.5;
                    else
                        Snd('Play',tone);
                    end
                elseif keyCode(leftKey)
                    % Decrease auditory frequency
                    if InitialFM>1.5
                        InitialFM=InitialFM-0.5;
                    else
                        Snd('Play',tone);
                    end
                elseif keyCode(returnKey)
                    Response=InitialFM;
                    Not_done = 0;
                    Not_done2 = 0;
                end
            end

            no_press = 0;
        end



        if GetSecs - Start_sound > Duration
            Not_done2 = 0;
        end

    end


    A=InitialLevel*ones(size(st,1),1);

    % Create the fade in and out functions
    FadeInFct=st(1:(Fs*FadeTime/1000))/st(Fs*FadeTime/1000);
    FadeOutFct=(st(size(st,1))-st((size(st,1)-Fs*FadeTime/1000):size(st,1)))/st(Fs*FadeTime/1000);

    % Get the faded signal
    A(1:Fs*FadeTime/1000)=FadeInFct.*A(1:Fs*FadeTime/1000);
    A((size(st,1)-Fs*FadeTime/1000):size(st,1))=FadeOutFct.*A((size(st,1)-Fs*FadeTime/1000):size(st,1));
    son=A.*sin(2*pi*ToneFreq(1,index)*st).*sin(2*pi*InitialFM*st);
    PsychPortAudio('Stop', pahandle);



    end;

    PsychPortAudio('Stop', pahandle);
    
    PsychPortAudio('Stop', pahandle);
    % Restore normal priority scheduling in case something else was set
    % before: