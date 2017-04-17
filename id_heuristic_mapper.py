id_heuristic_mapper = {
	# uses consolidate_runs_default
	'LLS:2.0.1026': 'default',
	'LLS:2.0.14': 'default',
	'LLS:2.0.15': 'default',
	'LLS:2.0.3': 'default',
	'LLS:2.0.4': 'default',
	'LLS:2.0.6': 'default',
	'LLS:2.0.7': 'default',
	'LLS:APLGSTDYBBL': 'default',
	'LLS:CATHSTUDYBIBLENT': 'default',
	'LLS:CONTBIBPATLIT_05_05': 'default',
	'LLS:ESVREFSTBBL': 'default',
	'LLS:EVDNCEBBLENTS': 'default', # <- maybe there's a better heuristic
	'LLS:EXPSTDYBBL': 'default',
	'LLS:FSB': 'default',
	'LLS:GSPLTRNSFRMTBBL': 'default',
	'LLS:JSB': 'default',
	'LLS:LIFEPRNCBIB': 'default',
	'LLS:NEWSFLLIFBBLNOTE': 'default',
	'LLS:PSTLCSTBJMSVRSN': 'default',
	'LLS:REVIVALSTBBL': 'default',
	'LLS:RFRMTNHRTGSTBBL': 'default',
	'LLS:RFRMTNSTSTNVRSN': 'default',
	'LLS:RYRIESBN-KJV': 'default',
	'LLS:RYRIESBN-NAS': 'default',
	'LLS:RYRIESBN-NIV': 'default',
	'LLS:SCOFIELDBBL1917': 'default',
	'LLS:UNGERBBLHB': 'default',
	# uses consolidate_runs_using_bold_heuristic
	'LLS:2.0.12': 'bold',
	'LLS:2.0.2': 'bold',
	'LLS:2.0.5': 'bold',
	'LLS:2.0.8': 'bold',
	'LLS:ANDREWSBNOTES': 'bold',
	'LLS:LSBCONCORDIA': 'bold',
	'LLS:CSB2ED': 'bold',
	'LLS:ESVGSBNOTES': 'bold',
	'LLS:ESVSB': 'bold',
	'LLS:NIVZNDRVNSTBBL': 'bold',
	'LLS:NKJVSTBIB': 'bold',
	'LLS:NLTSB': 'bold',
	'LLS:MACARTSBNASB': 'bold',
	# uses consolidate_runs_using_italics_heuristic
	'LLS:2.0.13': 'italics',
	'LLS:LSBCONCORDIA': 'italics'
}

id_paragraph_heuristic_mapper = {
	# consolidate paragraphs by heading text
	'LLS:LUCADOLLSB': 'heading_text',
	# consolidate paragraphs by milestone
	'LLS:2.0.19': 'milestone',
}
