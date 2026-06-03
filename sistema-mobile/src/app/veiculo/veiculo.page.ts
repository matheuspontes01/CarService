import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { LoadingController, NavController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';

import { Usuario } from '../home/usuario.models';
import { Veiculo } from './veiculo.model';

@Component({
  selector: 'app-veiculo',
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
  templateUrl: './veiculo.page.html',
  styleUrls: ['./veiculo.page.scss'],
  providers: [Storage],
})
export class VeiculoPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public veiculos: Veiculo[] = [];
  public carregandoLista = false;
  public mensagemErro = '';

  private storageReady?: Promise<Storage>;

  constructor(
    private storage: Storage,
    private controleCarregamento: LoadingController,
    private controleToast: ToastController,
    private controleNavegacao: NavController,
  ) {}

  async ngOnInit(): Promise<void> {
    const storage = await this.getStorage();
    const registro = await storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      await this.consultarVeiculosSistemaWeb();
    } else {
      this.controleNavegacao.navigateRoot('/home');
    }
  }

  private getStorage(): Promise<Storage> {
    if (!this.storageReady) {
      this.storageReady = this.storage.create();
    }

    return this.storageReady;
  }

  async consultarVeiculosSistemaWeb(): Promise<void> {
    this.carregandoLista = true;
    this.mensagemErro = '';

    const loading = await this.controleCarregamento.create({
      message: 'Pesquisando veiculos...',
      spinner: 'crescent',
    });

    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: 'http://127.0.0.1:8000/veiculo/api/listar/',
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 200 && Array.isArray(resposta.data)) {
          this.veiculos = resposta.data.map((veiculo: any) => Object.assign(new Veiculo(), veiculo));
        } else {
          this.veiculos = [];
          this.mensagemErro = 'Nao foi possivel carregar os veiculos cadastrados.';
          await this.exibirToast(this.mensagemErro);
        }

        await loading.dismiss();
        this.carregandoLista = false;
      })
      .catch(async (error) => {
        await loading.dismiss();
        this.carregandoLista = false;
        this.veiculos = [];
        this.mensagemErro = 'Erro ao consultar veiculos. Verifique o backend.';
        await this.exibirToast(this.mensagemErro);
        console.error('Erro ao consultar veículos:', error);
      });
  }

  obterFoto(url?: string): string {
    if (!url) {
      return 'assets/icon/favicon.png';
    }

    if (url.startsWith('http://') || url.startsWith('https://')) {
      return url;
    }

    return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
  }

  async atualizarLista(event?: CustomEvent): Promise<void> {
    await this.consultarVeiculosSistemaWeb();

    if (event?.target && 'complete' in event.target) {
      (event.target as HTMLIonRefresherElement).complete();
    }
  }

  private async exibirToast(mensagem: string): Promise<void> {
    const toast = await this.controleToast.create({
      message: mensagem,
      duration: 2000,
      position: 'bottom',
      color: 'dark',
    });

    await toast.present();
  }

}
