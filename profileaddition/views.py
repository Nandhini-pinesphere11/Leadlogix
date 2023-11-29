from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

@login_required
def profile_add(request):
    form_data = None

    # If it's a GET request, retrieve form_data based on the selected user
    selected_username = request.GET.get('selected_username')
    if selected_username:
        selected_user = User.objects.get(username=selected_username)
        form_data = Profile.objects.filter(user=selected_user).first()

    if request.method == 'POST':
        # Retrieve existing profile if it exists
        selected_username = request.POST.get('selected_username')
        print(f"Selected Username: {selected_username}")
        selected_user = User.objects.get(username=selected_username)

        form_data = Profile.objects.filter(user=selected_user).first()
        print(f"Form Data: {form_data}")
        # Gather form data
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone_country_code = request.POST.get('phone_country_code')
        phone_number = request.POST.get('phone_number')
        reference_number = request.POST.get('reference_number')
        contact_person = request.POST.get('contact_person')
        plan_name = request.POST.get('plan_name')
        address1 = request.POST.get('address1')
        state = request.POST.get('state')
        address2 = request.POST.get('address2')
        postcode = request.POST.get('postcode')
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        end_date = request.POST.get('end_date')

        # If a profile already exists, update it; otherwise, create a new one
        if form_data:
            form_data.company_name = company_name
            form_data.email = email
            form_data.phone_country_code = phone_country_code
            form_data.phone_number = phone_number
            form_data.reference_number = reference_number
            form_data.contact_person = contact_person
            form_data.plan_name = plan_name
            form_data.address1 = address1
            form_data.state = state
            form_data.address2 = address2
            form_data.postcode = postcode
            form_data.city = city
            form_data.from_date = from_date
            form_data.end_date = end_date
            form_data.save()
        else:
            Profile.objects.create(
                company_name=company_name,
                email=email,
                phone_country_code=phone_country_code,
                phone_number=phone_number,
                reference_number=reference_number,
                contact_person=contact_person,
                plan_name=plan_name,
                address1=address1,
                state=state,
                address2=address2,
                postcode=postcode,
                city=city,
                from_date=from_date,
                end_date=end_date,
                user=selected_user
            )

        return redirect('profile_add')

    # Get the 'Strings' group and its users
    strings_group = Group.objects.get(name='Strings')
    strings_group_users = strings_group.user_set.all()

    context = {
        'strings_group_users': strings_group_users,
        'state_choices': Profile.STATE_CHOICES,
        'form_data': form_data,
    }

    return render(request, 'profile/add_profile.html', context)




from django.core.exceptions import ObjectDoesNotExist

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def show_profile(request):
    try:
        # Retrieve the user's profile based on the logged-in user
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Handle the case where the profile does not exist
        user_profile = None  # or provide a default profile

    context = {'user_profile': user_profile}
    return render(request, 'profile/show_profile.html', context)



