#!D:/Python26/python.exe
# -*- coding: utf-8 -*-
'''
@author: josephzeng | josephzeng36@gmail.com
@copyright: v0.1
@copyright: 酷狗 2012
@version: v0.2
'''

import os
import re
import config as CONFIG
import subprocess
import func as func
import shlex

class CompressionCore:
    #mediainfo run exe where 
    mediainfo_run = str(CONFIG.MEDIAINFO) + " "

    #ffmpeg run exe where
    ffmpeg_run = str(CONFIG.FFMPEG)

    #mp4box run exe where
    mp4box_run = str(CONFIG.MP4BOX)

    #compression default
    compression_default = {'width':CONFIG.COMPRESSION_WIDTH,\
     'height':CONFIG.COMPRESSION_HEIGH}

    # get info
    mediainfo_info = ''

    # get ffmpeg info
    ffmpeg_info = ''

    # stdout info
    stdout = ""
    
    #logo param
    logo_param = {'name':'kugou.png', 'width':127, 'height':36, 'status':True} 
    
    def __init__(self):
        pass
    
    def add_video_logo(self, sfile = None):
        if self.logo_param['status'] == True:
            info = self.get_video_wh(sfile)
            video_w = info['video_w']
            video_h = info['video_h']
            logo_w = int(self.logo_param['width']) + 10
            logo_h = int(video_h) - 10
            res = ' -filter_complex "[0:0] pad=iw:ih [a];'+\
            '[a] scale='+str(video_w)+':'+str(video_h)+' [a1]; movie=kugou.png [b];'+\
            '[a1] [b] overlay=main_w-'+str(logo_w)+':main_h-'+str(logo_h)+'" '
            return res            
        else:
            return ''
            
    
    def get_video_rgb(self, sfile = None):
        '''
        get video color rgb
        '''
        if sfile != None:
            result = self.parse_mediainfo(sfile)
        else:
            result = self.mediainfo_info
        if result.get('video_chromasubsampling') != "":
            return True
        else:
            return False

    
    def get_video_framerate(self, sfile = None):
        ''' 
        get video frame rate
        '''
        if sfile == None:
           info = self.mediainfo_info
        else:
           info = self.parse_mediainfo(sfile)
        res = 25.00
        if info.get('video_framerate'):
            res = float(info['video_framerate'])
        return res
       
    def get_video_scantype(self, sfile = None):
        ''' 
        get video scan type 
        '''
        if sfile == None:
            info = self.mediainfo_info
        else:
            info = self.parse_mediainfo(sfile)
        
        if info['video_scantype'] == 'Progressive':
            return ''
        else:
            return ' -vf yadif=0:-1:1 '

    def get_video_wh(self, sfile = None):
        '''
        get video width and height
        '''
        if sfile != None:
            result = self.parse_mediainfo(sfile)
        else:
            result = self.mediainfo_info
        video_width = 768
        video_height = 432
        if result.get('video_width'):
            video_width = int(result.get('video_width'))
        if result.get('video_height'):
            video_height = int(result.get('video_height'))
        '''   
        if video_height >= self.compression_default['height']:
            height = self.compression_default['height']
	    width = self.compression_default['width']
	    percentage = height / float(self.compression_default['height'])
	    width = self.compression_default['width'] * float(percentage)
	    width = int(width)
        else:
            height = video_height
	    if video_width <= self.compression_default['width']:
		width = video_width
	    else:
		width = self.compression_default['width']
		percentage = height / float(self.compression_default['height'])
		width = self.compression_default['width'] * float(percentage)
		width = int(width)
        '''
        dd = float(self.compression_default['width'])/float(self.compression_default['height'])
        cc = float(video_width)/float(video_height)
        if cc <= dd:
            height = self.compression_default['height']
            width = cc * height
            width = int(width)
        else:
            width = self.compression_default['width']
            height = width / cc
            height = int(height)
	return {'video_w':width, 'video_h':height}
            
    def get_video_map(self, sfile = None):
        '''
        get video map
        '''
        if sfile != None:
            result = self.parse_ffmpeginfo(sfile)
        else:
            result = self.ffmpeg_info
        result['video_map'] = '0:0'
	result['audio_map'] = '0:1'
	data = {'video_map':' -map ' + str(result['video_map']), \
        'audio_map':' -map ' + str(result['audio_map'])}
	
        return data
    
    def parse_ffmpeginfo(self, sfile):
        '''
        get ffmpeg video info
        '''
        result = {
            'video_map':'0:0',
            'audio_map':'0:1'
        }
        args = self.ffmpeg_run + " -i " + str(sfile) + " 2>info_video.txt"
        os.popen(args).readlines()
        stdout = ''
        if os.path.isfile('info_video.txt') == True:
            fp = open('info_video.txt', 'r')
            stdout = fp.readlines()
            fp.close()
        mode = 'none'
        for line in stdout:
            line = line.strip()
            if 'Stream' in line:
                if line.find('Video') > 0:
                    value = line[8:11]
		    value = value.replace('.', ':')
                    func.set_par(result, 'video_map', value)
                if line.find('Audio') > 0:
                    value = line[8:11]
                    func.set_par(result, 'audio_map', value)
		    value = value.replace('.', ':')
                    break
        self.ffmpeg_info = result        
        return result
                    
    def parse_mediainfo(self, sfile):
        '''
        get mediainfo video info
        '''
        args = [self.mediainfo_run, '-f', sfile]
        output = subprocess.Popen(args, stdout=subprocess.PIPE).stdout
        data = output.readlines()
        output.close()
        mode = 'none'
        iscomplete = 0
        result = {
                'general_format' : '',
                'general_codec' : '',
                'general_size' : None,
                'general_bitrate' : None,
                'general_duration' : None,
                'is_general':'',
                'video_format' : '',
                'video_codec_id' : '',
                'video_codec' : '',
                'video_bitrate' : None,
                'video_width' : None,
                'video_height' : None,
                'video_displayaspect' : None,
                'video_pixelaspect' : None,
                'video_scantype' : '',
                'video_framerate': '',
                'video_colorspace': '',
                'video_chromasubsampling':'',
                'is_video':'',
                'audio_format' : '',
                'audio_codec_id' : '',
                'audio_codec' : '',
                'audio_bitrate' : None,
                'audio_channels' : None,
                'audio_samplerate' : None,
                'audio_resolution' : None,
                'audio_language' : '',
                'is_audio':''
                }
        for line in data:
            if not ':' in line:
                if 'General' in line:
                    mode = 'General'
                elif 'Video' in line:
                    mode = 'Video'
                elif 'Audio' in line:
                    mode = 'Audio'
                elif 'Text' in line:
                    mode = 'Text'
            else:
                key, sep, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                if mode == 'General':
                    if key == 'Format': func.set_par(result, 'general_format', value)
                    if key == 'Codec': func.set_par(result,'general_codec', value)
                    if key == 'File size': func.set_par(result,'general_size', value)
                    if key == 'Overall bit rate': func.set_par(result,'general_bitrate', value)
                    if key == 'Duration': func.set_par(result,'general_duration', value)
                    func.set_par(result,'is_general', 1)
                if mode == 'Video':
                    if key == 'Format': func.set_par(result,'video_format', value)
                    if key == 'Codec ID': func.set_par(result,'video_codec_id', value)
                    if key == 'Codec': func.set_par(result,'video_codec', value)
                    if key == 'Nominal bit rate': func.set_par(result,'video_bitrate', value)
                    if key == 'Width': func.set_par(result,'video_width', value)
                    if key == 'Height': func.set_par(result,'video_height', value)
                    if key == 'Display aspect ratio': func.set_par(result,'video_displayaspect', value)
                    if key == 'Pixel Aspect Ratio': func.set_par(result,'video_pixelaspect', value)
                    if key == 'Scan type': func.set_par(result,'video_scantype', value)
                    if key == 'Nominal frame rate': func.set_par(result,'audio_language', value)
                    if key == 'Frame rate': func.set_par(result,'video_framerate', value)
                    if key == 'Color space': func.set_par(result,'video_colorspace', value)
                    if key == 'Chroma subsampling': func.set_par(result,'video_chromasubsampling', value)
                    func.set_par(result,'is_video', 1)
                if mode == 'Audio':
                    if key == 'Format': func.set_par(result,'audio_format', value)
                    if key == 'Codec ID': func.set_par(result,'audio_codec_id', value)
                    if key == 'Codec': func.set_par(result,'audio_codec', value)
                    if key == 'Bit rate': func.set_par(result,'audio_bitrate', value)
                    if key == 'Channel(s)': func.set_par(result,'audio_channels', value)
                    if key == 'Sampling rate': func.set_par(result,'audio_samplerate', value)
                    if key == 'Resolution': func.set_par(result,'audio_resolution', value)
                    if key == 'Language': func.set_par(result,'audio_language', value)
                    func.set_par(result,'is_audio', 1)
        self.mediainfo_info = result
        return result

        
class CompressionByAvs(CompressionCore):
    '''
    compression by asv
    '''
    def __init__(self):
        '''
        construct
        '''
        CompressionCore.__init__(self)
        
    def todoMp4(self, sfile, dfile, bt = 1000000):
        '''
        to compression mp4
        '''
        CompressionCore.parse_mediainfo(self, sfile)
        CompressionCore.parse_ffmpeginfo(self, sfile)
        is_general = 0
        is_video = 0
        is_audio = 0
        if self.mediainfo_info['is_general'] !='':
	    is_general = int(self.mediainfo_info['is_general'])
        if self.mediainfo_info['is_video'] !='':
	    is_video = int(self.mediainfo_info['is_video'])
        if self.mediainfo_info['is_audio'] !='':
	    is_audio = int(self.mediainfo_info['is_audio'])	    
        if is_general == 1 and is_video == 1 and is_audio == 1:
            video_map = CompressionCore.get_video_map(self)
            video_wh = CompressionCore.get_video_wh(self)
            info_wh = 'LanczosResize('+str(video_wh['video_w'])+','+str(video_wh['video_h'])+')'
            video_scantype = CompressionCore.get_video_scantype(self)
            video_framerate = CompressionCore.get_video_framerate(self)
            video_colorrgb = CompressionCore.get_video_rgb(self)
            video_logo = CompressionCore.add_video_logo(self)
            
            ddsfile = sfile.replace('/','\\')
            #write avs file start
            fp = open('E:/video_cache/wmv.avs', 'w')
            strs = 'DirectShowSource("'+str(ddsfile)+'", fps='+str(video_framerate)+',convertfps=true)'
            fp.write(strs)
            if video_colorrgb == False:
                fp.write('\n')
                fp.write('ConvertToYV12()')
            fp.write('\n')
            fp.write(info_wh)
            fp.close()
            #end
            #run cmd
            #doit 1 pass
            res = 1
            run_cmd = self.ffmpeg_run + ' -i E:/video_cache/wmv.avs ' + str(video_map['video_map']) +\
                ' '+str(video_logo)+' -vcodec libx264 -b:v '+str(bt)+' '+\
                '-keyint_min 25 -deblock 2:-2 -x264opts keyint=30:me=esa '+\
                '-profile:v high -level 30 -r '+str(video_framerate)+' -pass 1 '+\
                '-f rawvideo -y NUL'
            func.setLogger().info(run_cmd)
            try:
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit 1 pass")
            
            #doit 2 pass
            run_cmd = self.ffmpeg_run + ' -i E:/video_cache/wmv.avs ' + str(video_map['video_map']) +\
                ' '+str(video_logo)+'-vcodec libx264 -b:v '+str(bt)+' '+\
                '-keyint_min 25 -deblock 2:-2 -x264opts keyint=30:me=esa '+\
                '-profile:v high -level 30 -r '+str(video_framerate)+' -pass 2 '+\
                ' -y E:/video_cache/temp2.mp4'
            func.setLogger().info(run_cmd)
            try:    
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit 2 pass")
                
            #doit aac
            run_cmd = self.ffmpeg_run + ' -i E:/video_cache/wmv.avs ' + str(video_map['audio_map']) +\
                ' -acodec "aac" -b:a 64000 -ac 2 -strict -2 -y E:/video_cache/temp2.aac'
            func.setLogger().info(run_cmd)
            try:    
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit aac")
                
            #doit mp4box video and aac
            run_cmd = self.mp4box_run + ' -add E:/video_cache/temp2.mp4  '+\
            '-add E:/video_cache/temp2.aac -fps '+str(video_framerate)+' -brand isom:1 -new '+str(dfile)
            func.setLogger().info(run_cmd)
            try:
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit aac")
            return res
        else:
            #video not complete
            func.setLogger().error("video not complete")
            #res = 2 not video format
            return 2

class CompressionByFFmpeg(CompressionCore):
    '''
    compression by asv
    '''
    def __init__(self):
        '''
        construct
        '''
        CompressionCore.__init__(self)
        
    def todoMp4(self, sfile, dfile, bt = 1000000):
        '''
        to compression mp4
        '''
        CompressionCore.parse_mediainfo(self, sfile)
        CompressionCore.parse_ffmpeginfo(self, sfile)
        is_general = 0
        is_video = 0
        is_audio = 0
        if self.mediainfo_info['is_general'] !='':
	    is_general = int(self.mediainfo_info['is_general'])
        if self.mediainfo_info['is_video'] !='':
	    is_video = int(self.mediainfo_info['is_video'])
        if self.mediainfo_info['is_audio'] !='':
	    is_audio = int(self.mediainfo_info['is_audio'])	    
        if is_general == 1 and is_video == 1 and is_audio == 1:
            video_map = CompressionCore.get_video_map(self)
            video_wh = CompressionCore.get_video_wh(self)
            info_wh = ' -vf "scale='+str(video_wh['video_w'])+':'+str(video_wh['video_h'])+'" '
	    info_wh = ''
            video_scantype = CompressionCore.get_video_scantype(self)
            video_framerate = CompressionCore.get_video_framerate(self)
            video_colorrgb = CompressionCore.get_video_rgb(self)
            video_logo = CompressionCore.add_video_logo(self)
            
            ddsfile = sfile.replace('/','\\')
            #run cmd
            #doit 1 pass
            res = 1
            run_cmd = self.ffmpeg_run + ' -i '+str(sfile)+' ' + str(video_map['video_map']) +\
                ' '+str(video_logo)+' -vcodec libx264 -b:v '+str(bt)+' '+str(info_wh)+' '+\
                '-keyint_min 25 -deblock 2:-2 -x264opts keyint=30:me=esa '+\
                '-profile:v high -level 30 -r '+str(video_framerate)+' -pass 1 '+\
                '-f rawvideo -y NUL'
            func.setLogger().info(run_cmd)
            try:
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit 1 pass")
            #doit 2 pass
            run_cmd = self.ffmpeg_run + ' -i '+str(sfile)+' ' + str(video_map['video_map']) +\
                ' '+str(video_logo)+'-vcodec libx264 -b:v '+str(bt)+' '+str(info_wh)+' '+\
                '-keyint_min 25 -deblock 2:-2 -x264opts keyint=30:me=esa '+\
                '-profile:v high -level 30 -r '+str(video_framerate)+' -pass 2 '+\
                ' -y E:/video_cache/temp2.mp4'
            func.setLogger().info(run_cmd)
            try:    
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit 2 pass")
                
            #doit aac
            run_cmd = self.ffmpeg_run + ' -i ' + sfile + ' ' + str(video_map['audio_map']) +\
                ' -acodec "aac" -b:a 64000 -ac 2 -strict -2 -y E:/video_cache/temp2.aac'
            func.setLogger().info(run_cmd)
            try:    
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit aac")
                
            #doit mp4box video and aac
            run_cmd = self.mp4box_run + ' -add E:/video_cache/temp2.mp4  '+\
            '-add E:/video_cache/temp2.aac -fps '+str(video_framerate)+' -brand isom:1 -new '+str(dfile)
            func.setLogger().info(run_cmd)
            try:
                output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).stdout
                data = output.readlines()
                output.close()
            except:
                res = 0
                func.setLogger().error("Exception doit aac")
            #res = 0 except  res = 1 success
            return res
        else:
            #video not complete
            func.setLogger().error("video not complete")
            #res = 2 not video format
            return 2 
        
		
