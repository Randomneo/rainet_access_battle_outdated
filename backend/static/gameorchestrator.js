import { Events } from './event.js';


export class GameOrchestrator {
    /*
      Core class responsible for ingame time managment players turns.
      connecting with external endpoints etc.
     */
    constructor (board) {
        let self = this;
        this.board = board;
        this.playerTurn = false;
        this.socket = null;

        Events.handlers('game.send_move').set('send_move', data => self.sendMove(data));
        Events.handlers('board.start').set('send_layout', data => self.sendLayout(data));
    }

    bindSocket(socket) {
        this.socket = socket;
        this.socket.onmessage = this.catchSocket;
    }

    catchSocket(messageEvent) {
        let data = JSON.parse(messageEvent.data);
        console.log(data);
        switch (data.type) {
        case 'error': console.log(data.message); break;
            // todo redirect to some action on board
        case 'action': console.log(data.action); break;
        default:
            console.log(`Unknown socket message type ${data.type}`);
            break;
        }
    }

    moveEnemy(from, to) {
        this.board.vset(to, this.board.vget(from));
        this.board.vset(from, null);
    }

    sendMove(data) {
        // send move to server
        console.log('sending move. data: ');
        console.log(JSON.stringify(data));
        this.socket.send(JSON.stringify({
            type: 'move',
            data: data,
        }));
    }

    sendLayout(data) {
        function transpose(matrix) {
            return matrix[0].map((col, i) => matrix.map(row => row[i]));
        }
        let board_to_send = transpose(data.board).map(x => x.map(y => y ? y.name : '_'));
        console.log(JSON.stringify(board_to_send));
        this.socket.send(JSON.stringify({
            type: 'layout',
            data: board_to_send,
        }));
    }

}
