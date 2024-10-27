from django.http import FileResponse, HttpResponse
import mimetypes
from django.shortcuts import render
import wikipediaapi
import os
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def get_search(search):
    wiki = wikipediaapi.Wikipedia('WikiSearchApp (khushikoriya118@gmail.com)','en')
    page = wiki.page(search)
    if not page.exists():
        return None
    return page.summary

def save_file(search, summary):
    file_dir = os.path.join(settings.MEDIA_ROOT, 'summaries')
    os.makedirs(file_dir, exist_ok=True)

    file_name = f"{search}_summary.txt"
    file_path = os.path.join(file_dir, file_name)

    content = f"=== Summary for: {search} ===\n\nSummary:\n{summary}\n\n=== End of Summary ==="
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"summaries/{file_name}"

def handle_search(request):
    if request.method == 'POST':
        word = request.POST.get('search')
        if word: 
            summary = get_search(word)
            if summary:
                file_url = save_file(word, summary)
                return render(request, 'index.html', {'summary': summary, 'filename': file_url})
            else:
                return render(request, 'index.html', {'error': "Sorry, no Wikipedia page found for the given word!"})
        else:
            return render(request, 'index.html', {'error': "Please enter a search term."})
    else:
        return HttpResponse("Invalid request method! Please use POST to submit your search.")


def download_summary(request, file_path):
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    
    if not os.path.exists(absolute_file_path):
        return HttpResponse("Sorry, the file does not exist.")

    
    mime_type, _ = mimetypes.guess_type(absolute_file_path)
    response = FileResponse(open(absolute_file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(absolute_file_path)}'
    
    return response
