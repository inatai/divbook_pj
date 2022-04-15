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
	// 「OK」時の処理開始 ＋ 確認ダイアログの表示
	if(window.confirm('予約不可にしますか？')){
		return true;
	}
	// 「キャンセル」時の処理開始
	else{
		window.alert('キャンセルされました');
                return false; // 警告ダイアログを表示
	}
}

function disp_item_del(){
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
