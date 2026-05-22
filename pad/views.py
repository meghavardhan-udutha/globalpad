from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import re

from .models import Pad, PadFile


def index(request):
    return render(request, 'pad/index.html')


def access_view(request):
    return render(request, 'pad/access.html')


def upload_view(request):
    return render(request, 'pad/upload.html')


# ─── REST API ────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET"])
def api_access_pad(request, code):
    """Retrieve pad content by code."""
    code = code.strip().upper()
    try:
        pad = Pad.objects.prefetch_related('files').get(code=code)
    except Pad.DoesNotExist:
        return JsonResponse({'error': 'Invalid code. No pad found.'}, status=404)

    files_data = []
    for f in pad.files.all():
        files_data.append({
            'id': f.id,
            'name': f.original_name,
            'size': f.get_size_display(),
            'type': f.file_type,
            'url': f.file.url,
        })

    return JsonResponse({
        'code': pad.code,
        'text': pad.text_content,
        'files': files_data,
        'created_at': pad.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': pad.updated_at.strftime('%Y-%m-%d %H:%M'),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_upload_pad(request):
    """Create or update a pad with text and/or files."""
    code = request.POST.get('code', '').strip().upper()
    text = request.POST.get('text', '').strip()
    files = request.FILES.getlist('files')

    if not code:
        return JsonResponse({'error': 'Code is required.'}, status=400)

    if not re.match(r'^[A-Z0-9\-_]{3,20}$', code):
        return JsonResponse({
            'error': 'Code must be 3–20 characters: letters, numbers, hyphens, underscores only.'
        }, status=400)

    pad, created = Pad.objects.get_or_create(code=code)

    if text:
        pad.text_content = text
        pad.save()

    saved_files = []
    for f in files:
        pad_file = PadFile(pad=pad, original_name=f.name, file=f)
        pad_file.save()
        saved_files.append({
            'name': pad_file.original_name,
            'size': pad_file.get_size_display(),
            'type': pad_file.file_type,
        })

    return JsonResponse({
        'success': True,
        'code': pad.code,
        'created': created,
        'files_uploaded': len(saved_files),
        'files': saved_files,
        'message': f"Pad {'created' if created else 'updated'} successfully."
    }, status=201 if created else 200)


@require_http_methods(["GET"])
def api_download_file(request, file_id):
    """Download a specific file by ID."""
    pad_file = get_object_or_404(PadFile, id=file_id)
    try:
        response = FileResponse(
            pad_file.file.open('rb'),
            as_attachment=True,
            filename=pad_file.original_name
        )
        return response
    except FileNotFoundError:
        raise Http404("File not found on disk.")
