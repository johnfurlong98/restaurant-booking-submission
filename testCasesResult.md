venvjohnfurlong@Johns-MacBook-Air restaurant-booking-submission % python -m pytest reservations/tests/ -v
=========================================== test session starts ============================================
platform darwin -- Python 3.9.21, pytest-8.0.0, pluggy-1.5.0 -- /Users/johnfurlong/Desktop/submission/restaurant-booking-submission/venv/bin/python
cachedir: .pytest_cache
django: version: 4.2.11, settings: restaurant_reservations.test_settings (from ini)
rootdir: /Users/johnfurlong/Desktop/submission/restaurant-booking-submission
configfile: pytest.ini
plugins: cov-4.1.0, django-4.8.0, Faker-37.0.0
collected 16 items                                                                                         

reservations/tests/test_forms.py::TestReservationForm::test_valid_reservation_form PASSED            [  6%]
reservations/tests/test_forms.py::TestReservationForm::test_invalid_party_size PASSED                [ 12%]
reservations/tests/test_forms.py::TestReservationForm::test_past_date_reservation PASSED             [ 18%]
reservations/tests/test_models.py::TestTableModel::test_table_creation PASSED                        [ 25%]
reservations/tests/test_models.py::TestTableModel::test_table_availability PASSED                    [ 31%]
reservations/tests/test_models.py::TestReservationModel::test_reservation_creation PASSED            [ 37%]
reservations/tests/test_models.py::TestReservationModel::test_invalid_party_size PASSED              [ 43%]
reservations/tests/test_models.py::TestReservationModel::test_duplicate_reservation_time PASSED      [ 50%]
reservations/tests/test_urls.py::TestUrls::test_reservation_create_url PASSED                        [ 56%]
reservations/tests/test_urls.py::TestUrls::test_reservation_list_url PASSED                          [ 62%]
reservations/tests/test_urls.py::TestUrls::test_reservation_cancel_url PASSED                        [ 68%]
reservations/tests/test_urls.py::TestUrls::test_url_names PASSED                                     [ 75%]
reservations/tests/test_views.py::TestReservationViews::test_reservation_create_view PASSED          [ 81%]
reservations/tests/test_views.py::TestReservationViews::test_reservation_list_view PASSED            [ 87%]
reservations/tests/test_views.py::TestReservationViews::test_reservation_cancel_view PASSED          [ 93%]
reservations/tests/test_views.py::TestReservationViews::test_unauthorized_reservation_access PASSED  [100%]

============================================ 16 passed in 0.26s ============================================
venvjohnfurlong@Johns-MacBook-Air restaurant-booking-submission % 