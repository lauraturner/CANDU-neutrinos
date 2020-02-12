"# CANDU-neutrinos" 
DataBase Units:
	Database name:	'reactors'
		Collection names: 
				'BRUCEA-G1'
			'	'BRUCEA-G2'
				'BRUCEA-G3'
				'BRUCEA-G4'
				'BRUCEB-G5'
				'BRUCEB-G6'
				'BRUCEB-G7'
				'BRUCEB-G8'
				'DARLINGTON-G1'
				'DARLINGTON-G2'
				'DARLINGTON-G3'
				'DARLINGTON-G4'
				'PICKERINGA-G1'
				'PICKERINGA-G4'
				'PICKERINGB-G5'
				'PICKERINGB-G6'
				'PICKERINGB-G7'
				'PICKERINGB-G8'
		Data Units: (for all collections)
			date: [date time]
			thermal_pwr: [MWh/day]

	Database name:	'fission_data'
		Collection name: 
			'fission_fractions'
		Data Units:
			days: [days]
			U235: [fraction of total fuel fissions]
			U238: [fraction of total fuel fissions]
			Pu239: [fraction of total fuel fissions]
			Pu241: [fraction of total fuel fissions]

		Collection name: 
			'fission_rates'
		Data Units:
			days: [days]
			U235: [fissions/s] ???? need to double check these
			U238: [fissions/s]
			Pu239: [fissions/s]
			Pu241: [fissions/s]

		Collection name: 
			'nu_spectrum_candu'
		Data Units:
			energy_MeV: [MeV]
			U235: [#nu per MeV per fission] 
			U238: [#nu per MeV per fission]
			Pu239: [#nu per MeV per fission]
			Pu241: [#nu per MeV per fission]



