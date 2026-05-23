import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AlertController, IonButton, IonContent, IonInput, IonItem, IonList, IonToolbar, LoadingController, NavController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonButton, IonContent, IonToolbar, IonList, IonItem, FormsModule, IonInput],
})
export class HomePage {
  
  public instancia: { username: string; password: string } = {
    username: '',
    password: '',
  };

  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_alerta: AlertController,
    public controle_toast: ToastController,
   ) {}

  public entrar(): void {
    alert(`Tentando entrar com ${this.instancia.username}`);
  }

  async autenticarUsuario() {}
}
