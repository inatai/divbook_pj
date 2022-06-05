function disp_del(){
	// 「OK」時の処理開始 ＋ 確認ダイアログの表示
	if(window.confirm('消去しますか？')){
		return true;
	}
	// 「キャンセル」時の処理開始
	else{
		window.alert('キャンセルされました');
                return false; // 警告ダイアログを表示
	}
}

function disp_hol(){
	if(window.confirm('予約不可にしますか？')){
		return true;
	}
	else{
		window.alert('キャンセルされました');
                return false;
	}
}

function disp_item_del(){
	if(window.confirm('消去しますか？')){
		return true;
	}
	else{
		window.alert('キャンセルされました');
                return false;
	}
}

function disp_book(){
	if(window.confirm('予約しますか？')){
		return true;
	}
	else{
		window.alert('キャンセルされました');
                return false;
	}
}
