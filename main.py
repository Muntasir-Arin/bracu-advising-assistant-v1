import program
import fetch

# fetch.start() or use realtime_fetch for getting data directly from usis

preferred_course= ["cse321", "cse370", "cse426", "cse427", "cse470", "che101"]
preferred_sections=None #{"mat215": [1,2]}
availability_check= False
must= None
# program.course_suggest(preferred_course, None, False, course_num=6,lab=2, top=100, must=must)
program.main_function(preferred_course, preferred_sections, availability_check, 20)