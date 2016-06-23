#from openerp import models, fields, api
from openerp.osv import osv, fields
import datetime
GENDER_SELECTION = [('male','Male'),('female','Female'),('homosexual','Homosexual')]


class Student(osv.Model):
	_name = 'openacademy.student'
	_columns = {
		#'student_id' : fields.integer('Student\'ID', required=True),
		'student_name' : fields.char('Student\'s name', size=128, required=True),
		'gender' : fields.selection(GENDER_SELECTION,string='Gender'),
		'date' : fields.date('Date of Birth', required=True),
		'course_ids' : fields.many2many('openacademy.course','course_student_rel','student_id','course_id')

	}

class Course(osv.Model):
	_name = 'openacademy.course'

	def totalstudents(self,cr,uid,ids,field,arg,context=None):
		res = {}
		for obj in self.browse(cr,uid,ids,context=context):
			total = len(obj.student_ids)
			res[obj.id] = total
		return res

	_columns = {
		#'subject' : fields.char('Subject', size=128, required=True),
		#'course_id' : fields.integer('Subject\'s ID', required=True),
		'course_name' : fields.char('Subject', size=128, required=True),
		'credit' : fields.integer('Credit', required=True),
		'date' : fields.date('Date Started', required=True),
		'description' : fields.text('Description', required=True),
		'student_ids' : fields.many2many('openacademy.student','course_student_rel','course_id','student_id',string="Students"),
		'instructor_id' : fields.many2one('openacademy.instructor', ondelete='cascade', string="Instructed by"),
		'instructor_gender' : fields.related('instructor_id','gender',type='selection',selection=GENDER_SELECTION,readonly=True,string="Gender"),
		'total' : fields.function(totalstudents,type='integer',string='Number of students enrolled')
	}

	
	def create(self, cr, uid, vals, context=None):
		print vals
		vals['date'] = fields.date.today()
		res = super(Course, self).create(cr, uid, vals, context=context)
		
		return res



class Instructor(osv.Model):
	_name = 'openacademy.instructor'

	_columns = {
	'name' : fields.char('Instructor\'s name', size=128, required=True),
	'gender' : fields.selection([('male','Male'),('female','Female'),('homosexual','Homosexual')],string='Gender'),
	'course_ids' : fields.one2many('openacademy.course','instructor_id',string="Courses")

	}
