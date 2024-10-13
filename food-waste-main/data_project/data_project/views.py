# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .forms import userSignUpForm
from .models import SignUp, data, accepted, currentQuests
import pandas as pd
from datetime import timedelta
import random 
from .webcrawler2 import Prices, Items
import ollama
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import re
import cv2
import numpy as np

#Global Variables 

current_phone = []


def register_view (request):
    if request.method == 'POST':
        form = userSignUpForm(request.POST)
        if form.is_valid():
            # Generate a random 10-digit number for user_id
            random_user_id = random.randint(1000000000, 9999999999)

            # Create a new user instance without saving to the database yet
            new_user_profile = form.save(commit=False)

            # Assign the generated user_id to the user profile
            new_user_profile.user_id = random_user_id

            # Save the user profile to the database
            new_user_profile.save()

            return render(request, 'data_app/home.html')
        else:
            return render(request, 'data_app/register.html')
    else:
        form = userSignUpForm()
        return render(request, 'data_app/register.html', {'form': form})

def home_view (request):
    return render(request, 'data_app/home.html')

def login_view (request):
    if request.method == 'POST':
        form = userSignUpForm(request.POST)
        if form.is_valid():
            # Extract the phone attribute
            current_phone.append(int(form.cleaned_data['phone']))
    
        password = SignUp.objects.filter(password=request.POST.get('password'))

        return render(request, 'data_app/login.html', {'password': password})
    else:
        form = userSignUpForm()
        return render(request, 'data_app/login.html')

def create_quest_view(request):
    if request.method == 'POST':
        # Handle the form submission
        form = userSignUpForm(request.POST)
        if form.is_valid():
            # Fetch the user_id from the form input
            user_id = SignUp.objects.filter(user_id=request.POST.get('user_id')).first()  # Use .first() to avoid querying a queryset

            if user_id:
                valid = "false"
                # Create a new user instance without saving to the database yet
                new_user_profile = form.save(commit=False)

                # Assign the generated user_id to the user profile
                new_user_profile.user_id = user_id
                new_user_profile.valid = valid

                # Save the user profile to the database
                new_user_profile.save()

                # Pass items and prices to the context
                context = {
                    'items': Items,
                    'prices': Prices,
                }
                
                # Render the create quest page with the updated context
                return render(request, 'data_app/create_quest.html', context)
            
            else:
                # Handle case when user_id is not found
                form.add_error('user_id', 'User ID not found')

    else:
        # If the request method is GET, initialize a blank form
        form = userSignUpForm()

    # Pass items, prices, and form to the template for both GET and POST cases
    context = {
        'items': Items,
        'prices': Prices,
        'form': form,
    }

    # Render the 'create_quest' page, or handle form errors by returning the same page
    return render(request, 'data_app/create_quest.html', context)


def accepted_quests_view (request):

    accepted = accepted.objects.all()

    return render(request, 'data_app/accepted_quests.html',{'accepted':accepted})

def quest_list_view (request):

    user_id = currentQuests.objects.values_list('user_id', flat=True).distinct()
    concatenated_info = []

    
    # Convert to a list (array)
    unique_items_list = list(user_id)

    for i in unique_items_list:
        address = ""
        street = SignUp.objects.filter(user_id=i).values_list('street', flat=True)
        city = SignUp.objects.filter(user_id=i).values_list('city', flat=True)
        pin = str(SignUp.objects.filter(user_id=i).values_list('pincode', flat=True))

        address = street+city+pin

        current_address = SignUp.objects.filter(phone = current_phone[0]).values_list('address', flat=True)

        model = 'llama3.1'

        prompt = '''
        I have these two addresses. Please check and tell me if the distance between them is under 1 mile. If it is, just reply True and if it is more than or equal to 1 mile, just reply False. Do NOT say anything else at all.
        '''+"here are the two addresses:"+address+current_address

        stream = ollama.chat(
            model=model,
            messages=[{'role':'user', 'content':prompt}], 
            stream = True
        )

        reply = ""

        for chunk in stream:
            reply += chunk['message']['content']
        
        if reply == True:
            user_id = SignUp.objects.filter(user_id=user_id).first() 

        concatenated_info = concatenated_info + [list(user.values()) for user in user_id] 


    return render(request, 'data_app/quest_list.html',{'concatenated_info': concatenated_info})

def upload_receipt_view (request):

    # Optional: Set the path to tesseract.exe if not automatically found
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Open image file
    image_path = 'receipt.jpg'
    image = Image.open(image_path)

    # Convert image to grayscale
    gray_image = image.convert('L')

    # Convert the image to a numpy array for OpenCV processing
    gray_image_cv = np.array(gray_image)

    # reduce noise with Gaussian Blur
    # blurred_image = cv2.GaussianBlur(gray_image_cv, (3, 3), 0)

    # adaptive thresholding for contrast
    binary_image = cv2.threshold(gray_image_cv, 150, 255, cv2.THRESH_BINARY)

    # morphological operations to remove small noise
    # kernel = np.ones((1, 1), np.uint8)  
    # opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    # changes to binarizing the image
        # Apply thresholding to binarize the image
    _, binary_image = cv2.threshold(gray_image_cv, 150, 255, cv2.THRESH_BINARY)

    # Convert the binary image back to a PIL image for pytesseract
    binarized_image = Image.fromarray(binary_image)



    # Optional: Resize the image to enhance OCR accuracy (scale factor of 1.5 or 2 can be tested)
    # resized_image = binarized_image.resize((int(binarized_image.width * 2), int(binarized_image.height * 2)))

    # Extract text from the image using OCR with custom configurations
    custom_config = r'--oem 3 --psm 6'
    # Use the LSTM engine and assume a single uniform block of text
    extracted_text = pytesseract.image_to_string(binarized_image, config=custom_config)


    model = 'llama3.1'

    prompt = '''
    I have this image of a receipt in String format 
    Please tell me the index where the items of the receipt start to get listed and where they stop being listed in the string that I have given you. I don't want any explanation, just the start and end index seperated by a space inbetween. It  The String for the receipt is as follows
    ''' + extracted_text

    stream = ollama.chat(
        model=model,
        messages=[{'role':'user', 'content':prompt}], 
        stream = True
    )

    reply = ""

    for chunk in stream:
        reply += chunk['message']['content']
        

    prompt = """
    The start and end indices are given. Please tell me what the item names are as listed between these indices, and DO NOT include any other text, headers or introductions whatsover. Remove the item code and the items numbers. The start and end indices are as follows
    """ + reply + "This is the list" + extracted_text

    stream = ollama.chat(
        model=model,
        messages=[{'role':'user', 'content':prompt}], 
        stream = True
    )

    items_array = []
    var = ""

    for chunk in stream:
        if len(chunk['message']['content']) == 0 or chunk['message']['content'] == "\nGV":
            items_array.append(var)
            var = ""
        else:
            var += chunk['message']['content']

    cleaned_array = items_array[0].split('\n')

    allItemsString = ""

    for i in cleaned_array:
        allItemsString = allItemsString+str(i)

    itemVar = "Great Value Peanut Butter"

    prompt = """
    This is a list of the items given below, check if
    """ + itemVar + "exists in the array given. Interpret the abbreviations given for the items and ignore the other text. If there is a match, return true and if not, return false. DO NOT type anything else. This is the array" + allItemsString

    stream = ollama.chat(
        model=model,
        messages=[{'role':'user', 'content':prompt}], 
        stream = True
    )

    preserved_item = ""
    boolean = "0"
    for chunk in stream:
        boolean = str(chunk['message']['content'])
    
    if boolean != "0":
        quest = get_object_or_404(currentQuests, item=request.item, user=request.user)

        # Preserve the values you want to keep
        preserved_item = quest.item  # Preserving item
        value= quest.valid  # Preserving valid status
        preserved_user = quest.user_id

        # Delete the existing quest
        quest.delete()

        new_user = request.user  # Assuming you want to set the current user

        # Example of how you can create a new quest
        new_quest = currentQuests(
            item=preserved_item,
            user=preserved_user,
            valid="True" # Use the preserved valid status
        )
        new_quest.save()  # Save the new quest

        # Redirect to the my quests page after updating
        return redirect('my_quests')

    return render(request, 'data_app/upload_receipt.html')

def my_quests_view (request):
    user_quests = currentQuests.objects.filter(user=request.user) 

    return render(request, 'data_app/my_quests_view.html', {'user_quests': user_quests}) 

def navbar_view (request):

    return render(request, 'data_app/navbar.html')


from django.shortcuts import get_object_or_404

def delete_quest_view(request, item):
    if request.method == 'POST':
        quest = get_object_or_404(currentQuests, item=item, user=request.user)
        quest.delete()
    return redirect('my_quests')
