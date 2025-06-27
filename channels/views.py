import asyncio

from channels.models import Channels
from django.urls import reverse
from channels.models import Videos
from django.shortcuts import render, HttpResponseRedirect
from channels.forms import SendChannelForm
from django.contrib import messages
from  services.twitch import is_live

from asgiref.sync import sync_to_async

@sync_to_async
def get_user_channels(user):
    return list(Channels.objects.filter(user=user))


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = SendChannelForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            platform  = form.get_platform()

            if Channels.objects.filter(url=url,user = request.user).exists():
                messages.error(request, 'Канал  уже добавлен')
                return HttpResponseRedirect(reverse('channels'))

            if platform == 'twitch':
                name = form.get_twitch_name()
            else:
                messages.error(request, ' Платформа еще не добавлена')
                return HttpResponseRedirect(reverse('channels'))

            user = request.user
            if name and platform and name != 'NoName' and platform != 'error':
                Channels.objects.create(url=url, user=user, name=name, platform=platform)
                messages.success(request, 'Канал добавлен')
            else:
                messages.error(request, 'Ошибка при определении имени или платформы')
        else:
            messages.error(request, 'Форма содержит ошибки')
    else:
        form = SendChannelForm()
    context  = {'form': form}
    return render(request,'channels/home.html',context)


async def channels(request):
    AllChannels = await get_user_channels(request.user)

    tasks = [is_live(channel.name) for channel in AllChannels]
    statuses = await asyncio.gather(*tasks)

    for channel, status in zip(AllChannels, statuses):
        channel.status = status

    context = {
        'channels': AllChannels,
    }
    return render(request, 'channels/channels.html', context)


def videos(request):
    context = {
        'videos': Videos.objects.all(),
    }
    return render(request, 'channels/videos.html', context)