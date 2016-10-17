%GaborMotion23
% Moving Gabor with adjustable audio frequency


% Ef2xperimentInfo
ExperfimentName = {'GM22-Adj'};
%General Instruction
Instructions = {'Thank you for Your Participation';
    'You will be presented with contrasting lines and asked to adjust auditory frequency';
    'to corresond to the given spatial frequency.';
    ' ';
    'The "Right Key or d key" will make the auditory frequency faster.';
    'The "Left Key or a key" will make the auditory frequency slower.'; 
    'Press "f key" when you have finished adjusting. Then press the "Down or 2 key" to move on.';
    ' ';
    'Please click the mouse when you are ready to begin';};

% Sound Variables
Duration=0.5;
Fs=10000;   % Sample rate in Hz
FadeTime=50;   %Duration of fade function (ms)
st=(0:1/Fs:Duration)'; %
nrchannels = 1; % One channel only -> Mono sound.
repetitions = 0;
tone = MakeBeep(500,0.1);% extemes mark tone

% Visual Variables
gratingsize = 400;% By default the visible grating is 400 pixels by 400 pixels in size:
drawmask=1;% By default, we mask the grating by a gaussian transparency mask:
%f=0.09;% Grating cycles/pixel: By default 0.09 cycles per pixel.
%cyclespersecond=8 % Speed of grating in cycles per second: 8 cycle per second by default.
angle=0;% Angle of the grating: We default to 0 degrees.
texsize=gratingsize / 2;% Define Half-Size of the grating image.

% Keys
KbName('UnifyKeyNames');
rightKey = KbName('d'); %KbName('4');
leftKey = KbName('a');%KbName('6');
returnKey = KbName('f');
NextKey = kbName('s');

% Visual(f) and Speed(cyclespersecond) Matrices
low_freq_visual = repmat(.009,4,1);
low_freq_speed = repmat(1,4,1);
med_freq_visual = repmat(.04,4,1);
med_freq_speed = repmat(4,4,1);
high_freq_visual = repmat(.09,4,1);
high_freq_speed = repmat(8,4,1);
LeftMotion = repmat(100,4,1);
RightMotion = repmat(200,4,1);

% List
freq_matrix = zeros(72,3);
freq_matrix(1:4,:) = [low_freq_visual low_freq_speed LeftMotion];
freq_matrix(5:8,:) = [low_freq_visual med_freq_speed LeftMotion];
freq_matrix(9:12,:) = [low_freq_visual high_freq_speed LeftMotion];
freq_matrix(13:16,:) = [low_freq_visual low_freq_speed RightMotion];
freq_matrix(17:20,:) = [low_freq_visual med_freq_speed RightMotion];
freq_matrix(21:24,:) = [low_freq_visual high_freq_speed RightMotion];
freq_matrix(25:28,:) = [med_freq_visual low_freq_speed LeftMotion];
freq_matrix(29:32,:) = [med_freq_visual med_freq_speed LeftMotion];
freq_matrix(33:36,:) = [med_freq_visual high_freq_speed LeftMotion];
freq_matrix(37:40,:) = [med_freq_visual low_freq_speed RightMotion];
freq_matrix(41:44,:) = [med_freq_visual med_freq_speed RightMotion];
freq_matrix(45:48,:) = [med_freq_visual high_freq_speed RightMotion];
freq_matrix(49:52,:) = [high_freq_visual low_freq_speed LeftMotion];
freq_matrix(53:56,:) = [high_freq_visual med_freq_speed LeftMotion];
freq_matrix(57:60,:) = [high_freq_visual high_freq_speed LeftMotion];
freq_matrix(61:64,:) = [high_freq_visual low_freq_speed RightMotion];
freq_matrix(65:68,:) = [high_freq_visual med_freq_speed RightMotion];
freq_matrix(69:72,:) = [high_freq_visual high_freq_speed RightMotion];
Random_list = randperm(length(freq_matrix));

% Data Output
Data_GM22_Adj = zeros(72, 5);


%%

[Experiment Condition Participant Session] = ExperimentInfo(ExperimentName);
filename = [Experiment Condition Participant '.' Session];
 

 
try
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

    %% Screen
    
    
    % This script calls Psychtoolbox commands available only in OpenGL-based
    % versions of the Psychtoolbox. (So far, the OS X Psychtoolbox is the
    % only OpenGL-base Psychtoolbox.)  The Psychtoolbox command AssertPsychOpenGL will issue
    % an error message if someone tries to execute this script on a computer without
    % an OpenGL Psychtoolbox
    AssertOpenGL;
    
    % Get the list of screens and choose the one with the highest screen number.
    % Screen 0 is, by definition, the display with the menu bar. Often when
    % two monitors are connected the one without the menu bar is used as
    % the stimulus display.  Chosing the display with the highest dislay number is
    % a best guess about where you want the stimulus displayed.
    screens=Screen('Screens');
    screenNumber= max(screens);
    
    % Find the color values which correspond to white and black: Usually
    % black is always 0 and white 255, but this rule is not true if one of
    % the high precision framebuffer modes is enabled via the
    % PsychImaging() commmand, so we query the true values via the
    % functions WhiteIndex and BlackIndex:
    white=WhiteIndex(screenNumber);
    black=BlackIndex(screenNumber);
    
    % Round gray to integral number, to avoid roundoff artifacts with some
    % graphics cards:
    gray=round((white+black)/2);
    
    % This makes sure that on floating point framebuffers we still get a
    % well defined gray. It isn't strictly neccessary in this demo:
    if gray == white
        gray=white / 2;
    end
    
    % Contrast 'inc'rement range for given white and gray values:
    inc=white-gray;
    
    % Open a double buffered fullscreen window and set default background
    % color to gray:
    [w screenRect]=Screen('OpenWindow',screenNumber, gray);
    HideCursor;
    
    if drawmask
        % Enable alpha blending for proper combination of the gaussian aperture
        % with the drifting sine grating:
        Screen('BlendFunction', w, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    end
    
    PresentText( w , screenRect , Instructions, white)
    GetClicks;
    
    for current_trial = 1:length(freq_matrix)
        
        Rndm_start_param = randperm(length(PossibleFMs));
        
        InitialFM_start = PossibleFMs(Rndm_start_param(1));
        InitialFM = InitialFM_start;
        First_InitialFM = InitialFM;
        A = InitialLevel*ones(size(st,1),1);
        
        % Create the fade in and out functions
        FadeInFct=st(1:(Fs*FadeTime/1000))/st(Fs*FadeTime/1000);
        FadeOutFct=(st(size(st,1))-st((size(st,1)-Fs*FadeTime/1000):size(st,1)))/st(Fs*FadeTime/1000);
        
        % Get the faded signal
        A(1:Fs*FadeTime/1000)=FadeInFct.*A(1:Fs*FadeTime/1000);
        A((size(st,1)-Fs*FadeTime/1000):size(st,1))=FadeOutFct.*A((size(st,1)-Fs*FadeTime/1000):size(st,1));
        
        son=A.*sin(2*pi*ToneFreq(1,index)*st).*sin(2*pi*InitialFM*st);
        
        current_row = Random_list(current_trial);
        
        f = freq_matrix(current_row,1);
        cyclespersecond = freq_matrix(current_row,2);
        DirectionofMotion = freq_matrix(current_row,3);
        % Calculate parameters of the grating:
        
        % First we compute pixels per cycle, rounded up to full pixels, as we
        % need this to create a grating of proper size below:
        p=ceil(1/f);
        
        % Also need frequency in radians:
        fr=f*2*pi;
        
        % This is the visible size of the grating. It is twice the half-width
        % of the texture plus one pixel to make sure it has an odd number of
        % pixels and is therefore symmetric around the center of the texture:
        visiblesize=2*texsize+1;
        
        % Create one single static grating image:
        %
        % We only need a texture with a single row of pixels(i.e. 1 pixel in height) to
        % define the whole grating! If the 'srcRect' in the 'Drawtexture' call
        % below is "higher" than that (i.e. visibleSize >> 1), the GPU will
        % automatically replicate pixel rows. This 1 pixel height saves memory
        % and memory bandwith, ie. it is potentially faster on some GPUs.
        %
        % However it does need 2 * texsize + p columns, i.e. the visible size
        % of the grating extended by the length of 1 period (repetition) of the
        % sine-wave in pixels 'p':
        x = meshgrid(-texsize:texsize + p, 1);
        
        % Compute actual cosine grating:
        grating=gray + inc*cos(fr*x);
        
        % Store 1-D single row grating in texture:
        gratingtex=Screen('MakeTexture', w, grating);
        
        % Create a single gaussian transparency mask and store it to a texture:
        % The mask must have the same size as the visible size of the grating
        % to fully cover it. Here we must define it in 2 dimensions and can't
        % get easily away with one single row of pixels.
        %
        % We create a  two-layer texture: One unused luminance channel which we
        % just fill with the same color as the background color of the screen
        % 'gray'. The transparency (aka alpha) channel is filled with a
        % gaussian (exp()) aperture mask:
        mask=ones(2*texsize+1, 2*texsize+1, 2) * gray;
        [x,y]=meshgrid(-1*texsize:1*texsize,-1*texsize:1*texsize);
        mask(:, :, 2)=white * (1 - exp(-((x/90).^2)-((y/90).^2)));
        masktex=Screen('MakeTexture', w, mask);
        
        % Query maximum useable priorityLevel on this system:
        priorityLevel=MaxPriority(w); %#ok<NASGU>
        
        % We don't use Priority() in order to not accidentally overload older
        % machines that can't handle a redraw every 40 ms. If your machine is
        % fast enough, uncomment this to get more accurate timing.
        %Priority(priorityLevel);
        
        % Definition of the drawn rectangle on the screen:
        % Compute it to  be the visible size of the grating, centered on the
        % screen:
        dstRect=[0 0 visiblesize visiblesize];
        dstRect=CenterRect(dstRect, screenRect);
        
        % Query duration of one monitor refresh interval:
        ifi=Screen('GetFlipInterval', w);
        
        % Translate that into the amount of seconds to wait between screen
        % redraws/updates:
        
        % waitframes = 1 means: Redraw every monitor refresh. If your GPU is
        % not fast enough to do this, you can increment this to only redraw
        % every n'th refresh. All animation paramters will adapt to still
        % provide the proper grating. However, if you have a fine grating
        % drifting at a high speed, the refresh rate must exceed that
        % "effective" grating speed to avoid aliasing artifacts in time, i.e.,
        % to make sure to satisfy the constraints of the sampling theorem
        % (See Wikipedia: "Nyquist?Shannon sampling theorem" for a starter, if
        % you don't know what this means):
        waitframes = 1;
        
        % Translate frames into seconds for screen update interval:
        waitduration = waitframes * ifi;
        
        % Recompute p, this time without the ceil() operation from above.
        % Otherwise we will get wrong drift speed due to rounding errors!
        p=1/f;  % pixels/cycle
        
        % Translate requested speed of the grating (in cycles per second) into
        % a shift value in "pixels per frame", for given waitduration: This is
        % the amount of pixels to shift our srcRect "aperture" in horizontal
        % directionat each redraw:
        shiftperframe= cyclespersecond * p * waitduration;
        
        % Perform initial Flip to sync us to the VBL and for getting an initial
        % VBL-Timestamp as timing baseline for our redraw loop:
        vbl=Screen('Flip', w);
        
        i=0;
        
        Not_done = 1;
        while Not_done == 1;
            
            PsychPortAudio('FillBuffer', pahandle, son');
            PsychPortAudio('Start', pahandle, repetitions, 0, 1);
            Start_sound = GetSecs;
            % Animationloop:
            Not_done2 = 1;
            no_press =1;
            
            while Not_done2 == 1;
                
                
                
                
                % Shift the grating by "shiftperframe" pixels per frame:
                % the mod'ulo operation makes sure that our "aperture" will snap
                % back to the beginning of the grating, once the border is reached.
                % Fractional values of 'xoffset' are fine here. The GPU will
                % perform proper interpolation of color values in the grating
                % texture image to draw a grating that corresponds as closely as
                % technical possible to that fractional 'xoffset'. GPU's use
                % bilinear interpolation whose accuracy depends on the GPU at hand.
                % Consumer ATI hardware usually resolves 1/64 of a pixel, whereas
                % consumer NVidia hardware usually resolves 1/256 of a pixel. You
                % can run the script "DriftTexturePrecisionTest" to test your
                % hardware...
                xoffset = mod(i*shiftperframe,p);
                
                if DirectionofMotion == 100
                    i=i+1;
                elseif DirectionofMotion == 200
                    i=i-1;
                end
                
                % Define shifted srcRect that cuts out the properly shifted rectangular
                % area from the texture: We cut out the range 0 to visiblesize in
                % the vertical direction although the texture is only 1 pixel in
                % height! This works because the hardware will automatically
                % replicate pixels in one dimension if we exceed the real borders
                % of the stored texture. This allows us to save storage space here,
                % as our 2-D grating is essentially only defined in 1-D:
                srcRect=[xoffset 0 xoffset + visiblesize visiblesize];
                
                % Draw grating texture, rotated by "angle":
                Screen('DrawTexture', w, gratingtex, srcRect, dstRect, angle);
                
                if drawmask==1
                    % Draw gaussian mask over grating:
                    Screen('DrawTexture', w, masktex, [0 0 visiblesize visiblesize], dstRect, angle);
                end;
                
                % Flip 'waitframes' monitor refresh intervals after last redraw.
                % Providing this 'when' timestamp allows for optimal timing
                % precision in stimulus onset, a stable animation framerate and at
                % the same time allows the built-in "skipped frames" detector to
                % work optimally and report skipped frames due to hardware
                % overload:
                vbl = Screen('Flip', w, vbl + (waitframes - 0.5) * ifi);
                
                
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
        % Restore normal priority scheduling in case something else was set
        % before:
        
        Data_GM22_Adj(current_trial,1) = f;
        Data_GM22_Adj(current_trial,2) = DirectionofMotion;
        Data_GM22_Adj(current_trial,3) = cyclespersecond;
        Data_GM22_Adj(current_trial,4) = First_InitialFM;
        Data_GM22_Adj(current_trial,5) = Response;
        save(filename,'Data_GM22_Adj','-ASCII','-TABS')
        
        ITI(w , .1, gray)
        
        waitForKeyPress(NextKey)
        Priority(0);
        
    end
    
    %The same commands wich close onscreen and offscreen windows also close
    %textures.
    Screen('CloseAll');
    ShowCursor;
    
    
catch
    %this "catch" section executes in case of an error in the "try" section
    %above.  Importantly, it closes the onscreen window if its open.
    Screen('CloseAll');
    ShowCursor;
    PsychPortAudio('Stop', pahandle);

    Priority(0);
    psychrethrow(psychlasterror);
end %try..catch..


