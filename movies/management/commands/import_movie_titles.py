import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Tag, Field, Tag_Field, models, Movie, Movie_Title


class Command(BaseCommand):
	help = "Import movie titles translations."
	
	def add_arguments(self, parser):
		parser.add_argument('f', type=str,
		                    help='file path to import from')
		
		parser.add_argument(
			'--readonly',
			action='store_true',
			dest='readonly',
			help='Parse it without saving to database',
		)
	
	def handle(self, f, **options):
		df = pd.read_csv(f, delimiter='\t')
		progress = tqdm(total=len(df))
		for i, row in df.iterrows():
			try:
				if str(row.book_id).isdigit() and row.lang_id in ["HEB", "ENG"]:
					m = Movie.objects.get(bid=row.book_id)
					mt = Movie_Title(movie=m, title=row.title, lang=row.lang_id )
					if not options['readonly']:
						mt.save()
			except models.ObjectDoesNotExist:
				# log error to server?
				print("\nMovie was not found in DB, line=" + str(i))
			finally:
				progress.update(1)
		progress.close()
