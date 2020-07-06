from eztables.views import DatatablesView
from django.core.files.storage import DefaultStorage
from django.core.urlresolvers import reverse
from django.core.paginator import EmptyPage
from eztables.forms import DatatablesForm
from django.http import HttpResponseBadRequest



class EguideDatatablesForm(DatatablesForm):

    def __init__(self, *args, **kwargs):
        try:
            super(EguideDatatablesForm, self).__init__(*args, **kwargs)
        except (ValueError, UnicodeEncodeError):
            pass

class IfesDatatablesView(DatatablesView):

    def process_dt_response(self, data):
        try:
            self.form = EguideDatatablesForm(data)
        except KeyError:
            return HttpResponseBadRequest()

        if self.form.is_valid():
            self.object_list = self.get_queryset().values(*self.get_db_fields())
            try:
                return self.render_to_response(self.form)
            except EmptyPage:
                pass

        return HttpResponseBadRequest('Nothing to deplay');

    def render_to_response(self, form, **kwargs):
        '''Render Datatables expected JSON format'''
        storage = DefaultStorage()
        page = self.get_page(form)

        # My hack
        # Add image url to all fields indicated in the view class
        # using image_fields property
        try:
            for item in self.image_fields:
                for object_item in page.object_list:
                    object_item[item] = storage.url(object_item[item])
        except AttributeError:
            pass

        # Add hyperlink url to all fields indicated in the view class
        # using url_fields property
        try:
            for item in self.url_fields:
                for object_item in page.object_list:
                    object_item[item['field']] = [object_item[item['field']],
                                                  reverse(item['target'],
                                                          args=[object_item[item['arg']]]
                                                          ),
                                                  ]
        except AttributeError:
            pass

        data = {
            'iTotalRecords': page.paginator.count,
            'iTotalDisplayRecords': page.paginator.count,
            'sEcho': form.cleaned_data['sEcho'],
            'aaData': self.get_rows(page.object_list),
        }
        return self.json_response(data)



