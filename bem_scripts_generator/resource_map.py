from collections import defaultdict


memory = defaultdict(lambda: "2gb")

memory["citation_full_pubmed"] = "70mb"
memory["citation_full_cora"] = "75mb"
memory["coauthor_cs"] = "80mb"
memory["coauthor_physics"] = "140mb"
memory["facebook_pp"] = "110mb"
memory["twitch_de"] = "105mb"
memory["heterophilous_questions"] = "130mb"
memory["reddit2"] = "4gb"

time = defaultdict(lambda: "02:00:00")

# time values for 0.1 threshold
time["citation_full_pubmed"] = "00:04:00"
time["citation_full_cora"] = "00:06:00"
time["coauthor_cs"] = "00:07:00"
time["facebook_pp"] = "00:16:00"
time["twitch_de"] = "00:07:00"
time["coauthor_physics"] = "01:30:00"
time["eterophilous_questions"] = "00:30:00"
time["reddit2"] = "60:00:00"  # To be tuned
