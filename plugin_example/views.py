# TestY TMS - Test Management System
# Copyright (C) 2024 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
from testy.core.models import Project
from testy.tests_description.models import TestSuite
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import Serializer

from plugin_example.xlsx_parser_lib.xlsx_parser import XlsxParser


class ProjectListView(ListView):
    model = Project
    queryset = Project.objects.all()
    template_name = 'upload.html'
    context_object_name = 'projects'

class SuitListView(ListView):
    model = TestSuite
    queryset = TestSuite.objects.all()
    template_name = 'upload.html'
    context_object_name = 'suit'

class UploadFileApiView(CreateAPIView):
    serializer_class = Serializer

    def create(self, request, *args, **kwargs):
        project_model_name = request.POST.get('selector')
        testsuit_model_name = request.POST.get('testsuit_selector')
        project = get_object_or_404(Project, name=project_model_name)
        test_suit = get_object_or_404(TestSuite, name=testsuit_model_name)
        file = request.FILES.get('file')
        parser = XlsxParser(file, project.id, test_suit.name)
        try:
            suites_count, cases_count = parser.create_suites_with_cases()
            response_text = (
                f'{suites_count} created suites, '
                f'{cases_count} created cases'
            )
        except Exception as ex:
            response_text = f'An error occurred: {ex}'

        request.session['response'] = response_text
        return redirect(reverse('plugins:plugin_example:index'))
