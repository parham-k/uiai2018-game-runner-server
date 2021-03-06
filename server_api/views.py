import subprocess
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *

from server_api.models import Game, CompileRequest
from game_runner.server.server_runner import SERVER_FILE_NAME


@api_view(['GET'])
def get_server_status(request):
    if 'for_compile' in request.GET and request.GET['for_compile']:
        return Response({'message': 'READY'}, status=HTTP_200_OK)
    ps_output = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
    running_count = ps_output.stdout.decode('utf-8').count(SERVER_FILE_NAME)
    print(running_count)
    if running_count >= 8:
        return Response({'message': 'Overload, currently running {} games'.format(running_count)},
                        status=HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'READY', 'running': running_count}, status=HTTP_200_OK)


@api_view(['POST'])
def request_game(request):
    game = Game(
        game_id=int(request.data['game_id']),
        team1_name=request.data['team1_name'],
        team1_language=request.data['team1_language'].upper(),
        team1_code=request.data['team1_code'],
        team2_name=request.data['team2_name'],
        team2_language=request.data['team2_language'].upper(),
        team2_code=request.data['team2_code'],
    )
    game.save()
    game.run()
    return Response({'message': 'Game added to queue'}, HTTP_201_CREATED)


@api_view(['POST'])
def request_compile(request):
    code_id = request.data.get('id')
    code_file = request.data.get('code')
    code_language = request.data.get('language')

    compilation_request = CompileRequest(
        code_id=code_id,
        code_zip=code_file,
        language=code_language,
    )
    compilation_request.save()
    compilation_request.compile()
    return Response(compilation_request.get_callback_dict())
