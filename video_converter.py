#!/usr/bin/env python

import subprocess
import argparse
import sys
import os
import shutil
import datetime

script_location = os.path.dirname(os.path.realpath(__file__))
PROCESSING_FOLDER = os.path.join(os.environ.get('HOME'), 'Movies/Processing')
CONVERTED_FOLDER = os.path.join(os.environ.get('HOME'), 'Movies/Converted')
WATCH_FOLDER = os.path.join(os.environ.get('HOME'), 'PVR/Completed')
REJECT_FOLDER = os.path.join(os.environ.get('HOME'), 'Movies/Rejected')

# for mkv
# ffmpeg -i "input.mkv" -y -f mp4 -vcodec copy -ac 2 -c:a libfaac "output.m4v"

# for avi
#ffmpeg -i /Users/jzucker/PVR/Completed/the.simpsons.s07e07.king-size.homer.real.dvdrip.xvid-medieval\ 11.44.53\ PM.avi -vcodec libx264 /Users/jzucker/Desktop/simpsons.m4v

# number_of_args = 'Number of arguments: ' + str(len(sys.argv)) + ' arguments\n'
# arg_list = 'Argument List: ' + str(sys.argv) + '\n'

# test_file = open('/Users/jzucker/PVR/test/test_file.txt', 'w')
# test_file.write(number_of_args)
# test_file.write(arg_list)
# test_file.close()

def get_output_file_path(input_file_path, output_directory):
	movie_name = os.path.basename(input_file_path)
	print movie_name
	movie_directory = os.path.dirname(input_file_path)
	print movie_directory
	final_name = None
	if movie_name.endswith('.mkv'):
		final_name = movie_name.replace('.mkv', '.m4v')
	elif movie_name.endswith('.avi'):
		final_name = movie_name.replace('.avi', '.m4v')
	#final_name = movie_name.replace('.mkv', '.m4v')
	final_path = os.path.join(output_directory, final_name)
	return final_path

def convert_video(input_file_path, output_directory):
	print '*************'
	print 'input_file_path'
	print input_file_path
	final_path = get_output_file_path(input_file_path, output_directory)
	print 'final_path'
	print final_path
	conversion = subprocess.Popen(['ffmpeg', '-i', input_file_path, '-f', 'mp4', '-vcodec', 'copy', '-ac', '2', '-c:a', 'libfaac', final_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
	print conversion
	return conversion
	print '*************'

class MovieConverter():
	def __init__(self, **kwargs):
		pass
	def perform_conversion(self, **kwargs):
		print '-----------------'
		input_file_path = kwargs.get('input_file_path')
		output_directory = kwargs.get('output_directory', CONVERTED_FOLDER)
		conversion_process = convert_video(input_file_path, output_directory)
		print conversion_process
		print '-----------------'
		return conversion_process

class MovieListCollector():
	def __init__(self, **kwargs):
		self.search_folder = kwargs.get('search_folder', WATCH_FOLDER)
		self.movies = []
	def get_full_path(self, item):
		return os.path.join(self.search_folder, item)
	def get_all_folders(self):
		print 'get_all_folders'
		folders = []
		for folder in os.listdir(self.search_folder):
			if os.path.isdir(self.get_full_path(folder)):
				folders.append(self.get_full_path(folder))
		return folders
	def get_movie_from_folder(self, folder):
		print 'get_movie_from_folder'
		for item in os.listdir(folder):
			if ((item.endswith('.mkv')) or item.endswith('.avi')) and (item.find('sample') ==-1):
				full_path = os.path.join(folder, item)
				self.movies.append(full_path)
		print self.movies
	def get_all_new_movies(self):
		folders = self.get_all_folders()
		for folder in folders:
			self.get_movie_from_folder(folder)
		return self.movies

class CompletedFolderHandler():
	def __init__(self, **kwargs):
		self.processing_folder = kwargs.get('processing_folder', PROCESSING_FOLDER)
		self.movie_collector = MovieListCollector(search_folder=WATCH_FOLDER)
		self.converter = MovieConverter()
	def move_for_processing(self, movie_path):
		movie_name = os.path.basename(movie_path)
		old_directory = os.path.dirname(movie_path)
		new_path = os.path.join(self.processing_folder, movie_name)
		shutil.move(movie_path, new_path)
		shutil.rmtree(old_directory)
		return new_path
	def process_movies(self):
		print 'processing_movies'
		for movie in self.movie_collector.get_all_new_movies():
			processing_movie = self.move_for_processing(movie)
			print 'processing_movie'
			print processing_movie
			new_movie = self.converter.perform_conversion(input_file_path=processing_movie, output_directory=CONVERTED_FOLDER)



def main():
	print str(datetime.datetime.now())
	completed_folder_handler = CompletedFolderHandler(processing_folder=PROCESSING_FOLDER)
	completed_folder_handler.process_movies()


if __name__ == '__main__':
	main()