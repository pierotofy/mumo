import alsaaudio

def get_mixer(name, **kwargs):
    # Demonstrates how mixer settings are queried.
    result = {}
    try:
        mixer = alsaaudio.Mixer(name, **kwargs)
    except alsaaudio.ALSAAudioError:
        print("No such mixer", file=sys.stderr)
        sys.exit(1)

    result['volumecap'] = mixer.volumecap()
    result['switchcap'] = mixer.switchcap()
    result['volumes'] = mixer.getvolume()
        
    try:
        result['mutes'] = mixer.getmute()
    except alsaaudio.ALSAAudioError:
        # May not support muting
        pass

    try:
        result['recs'] = mixer.getrec()
    except alsaaudio.ALSAAudioError:
        # May not support recording
        pass

    return result

def set_mixer(name, args, **kwargs):
    # Demonstrates how to set mixer settings
    try:
        mixer = alsaaudio.Mixer(name, **kwargs)
    except alsaaudio.ALSAAudioError:
        print("No such mixer", file=sys.stderr)
        sys.exit(1)

    if args.find(',') != -1:
        args_array = args.split(',')
        channel = int(args_array[0])
        args = ','.join(args_array[1:])
    else:
        channel = alsaaudio.MIXER_CHANNEL_ALL

    if args in ['mute', 'unmute']:
        # Mute/unmute the mixer
        if args == 'mute':
            mixer.setmute(1, channel)
        else:
            mixer.setmute(0, channel)
        
    elif args in ['rec','unrec']:
        # Enable/disable recording
        if args == 'rec':
            mixer.setrec(1, channel)
        else:
            mixer.setrec(0, channel)

    else:
        # Set volume for specified channel. MIXER_CHANNEL_ALL means set
        # volume for all channels
        volume = int(args)
        mixer.setvolume(volume, channel)