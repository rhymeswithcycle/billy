from django import forms
from django.conf import settings

from billy.models import db, Metadata, DoesNotExist


def get_region_select_form(data):
    abbrs = [('', '')]
    for abbr in sorted(settings.ACTIVE_STATES):
        try:
            obj = Metadata.get_object(abbr)
            abbrs.append((obj['_id'], obj['name']))
        except DoesNotExist:
            # ignore missing
            pass

    class RegionSelectForm(forms.Form):
        abbr = forms.ChoiceField(choices=abbrs, label="abbr")

    return RegionSelectForm(data)


class FindYourLegislatorForm(forms.Form):
    address = forms.CharField()


def get_filter_bills_form(metadata):

    class FilterBillsForm(forms.Form):

        search_text = forms.CharField(required=False)

        # `metadata` will be None if the search is across all bills
        if metadata:
            _bill_types = metadata.distinct_bill_types()
            _bill_subjects = metadata.distinct_bill_subjects()
            _bill_sponsors = [(leg['_id'], leg.display_name()) for leg in
                              metadata.legislators()]
            _sessions = [(s['id'], s['name']) for s in metadata.sessions()]

            BILL_TYPES = [('', '')] + zip(_bill_types, [s.title()
                                                        for s in _bill_types])
            BILL_SUBJECTS = [('', '')] + zip(_bill_subjects, _bill_subjects)
            BILL_SPONSORS = [('', '')] + _bill_sponsors
            SESSIONS = [('', '')] + _sessions

            session = forms.ChoiceField(choices=SESSIONS, required=False)

            _status_choices = [('', '')]
            if 'lower_chamber_name' in metadata:
                _status_choices.append(('passed_lower',
                                'Passed ' + metadata['lower_chamber_name']))
            if 'upper_chamber_name' in metadata:
                _status_choices.append(('passed_upper',
                                'Passed ' + metadata['upper_chamber_name']))
            _status_choices.append(('signed', 'Signed'))

            if len(_status_choices) == 4:
                chamber = forms.MultipleChoiceField(
                            choices=(
                                ('upper', metadata['upper_chamber_name']),
                                ('lower', metadata['lower_chamber_name'])
                            ),
                            widget=forms.CheckboxSelectMultiple(),
                            required=False)

            sponsor__leg_id = forms.ChoiceField(choices=BILL_SPONSORS,
                                                required=False,
                                                label='Sponsor name')

        else:
            _bill_types = db.bills.distinct('type')
            _bill_subjects = db.bills.distinct('subjects')

            BILL_TYPES = [('', '')] + zip(_bill_types,
                                          [s.title() for s in _bill_types])
            BILL_SUBJECTS = [('', '')] + zip(_bill_subjects, _bill_subjects)

            chamber = forms.MultipleChoiceField(
                        choices=(('upper', 'upper'),
                                 ('lower', 'lower')),
                        widget=forms.CheckboxSelectMultiple(),
                        required=False)

            status = forms.ChoiceField(
                        choices=(
                            ('', ''),
                            ('passed_lower', 'Passed lower'),
                            ('passed_upper', 'Passed upper'),
                            ('signed', 'Signed'),
                        ), required=False)

        type = forms.ChoiceField(choices=BILL_TYPES, required=False)

        subjects = forms.MultipleChoiceField(choices=BILL_SUBJECTS,
                                             required=False,
                #widget=forms.CheckboxSelectMultiple()
                #widget=FilteredSelectMultiple("Subjects", is_stacked=False)
                    )

    return FilterBillsForm
