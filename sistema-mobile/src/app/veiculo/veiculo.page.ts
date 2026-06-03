import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { AlertButton, LoadingController, NavController, ToastController } from '@ionic/angular';
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
  public mostrarEdicaoVeiculo = false;
  public carregandoEdicao = false;
  public salvandoEdicao = false;
  public veiculoEditando: Veiculo = new Veiculo();
  public mostrarConfirmacaoExclusao = false;
  public veiculoSelecionado: Veiculo | null = null;
  public marcas = [
    { valor: 1, label: 'AUDI' },
    { valor: 2, label: 'BMW' },
    { valor: 3, label: 'CHEVROLET - GM' },
    { valor: 4, label: 'FERRARI' },
    { valor: 5, label: 'FIAT' },
    { valor: 6, label: 'FORD' },
    { valor: 7, label: 'HONDA' },
    { valor: 8, label: 'HYUNDAI' },
    { valor: 9, label: 'VOLKSWAGEN' },
    { valor: 10, label: 'PORSCHE' },
  ];
  public cores = [
    { valor: 1, label: 'BRANCO' },
    { valor: 2, label: 'AMARELO' },
    { valor: 3, label: 'AZUL' },
    { valor: 4, label: 'PRATA' },
    { valor: 5, label: 'PRETO' },
    { valor: 6, label: 'VERMELHO' },
  ];
  public combustiveis = [
    { valor: 1, label: 'GASOLINA' },
    { valor: 2, label: 'DIESEL' },
    { valor: 3, label: 'FLEX' },
    { valor: 4, label: 'GNV' },
  ];
  public botoesConfirmacaoExclusao: AlertButton[] = [
    {
      text: 'Cancelar',
      role: 'cancel',
      handler: () => this.fecharConfirmacaoExclusao(),
    },
    {
      text: 'Excluir',
      role: 'destructive',
      handler: () => this.confirmarExclusaoVeiculo(),
    },
  ];

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
    } else {
      this.controleNavegacao.navigateRoot('/home');
    }
  }

  async ionViewWillEnter(): Promise<void> {
    if (this.usuario.token) {
      await this.consultarVeiculosSistemaWeb();
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

  abrirConfirmacaoExclusao(veiculo: Veiculo): void {
    this.veiculoSelecionado = veiculo;
    this.mostrarConfirmacaoExclusao = true;
  }

  async editarVeiculo(veiculo: Veiculo): Promise<void> {
    if (!veiculo.id) {
      await this.exibirToast('Nao foi possivel abrir a edicao deste veículo.');
      return;
    }

    this.carregandoEdicao = true;

    const loading = await this.controleCarregamento.create({
      message: 'Carregando veículo...',
      spinner: 'crescent',
    });

    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/veiculo/api/editar/${veiculo.id}/`,
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 200 && resposta.data) {
          this.veiculoEditando = Object.assign(new Veiculo(), resposta.data);
          this.mostrarEdicaoVeiculo = true;
        } else {
          await this.exibirToast('Nao foi possivel carregar os dados do veículo.');
        }

        await loading.dismiss();
        this.carregandoEdicao = false;
      })
      .catch(async (error) => {
        console.error('Erro ao carregar veículo para edição:', error);
        await loading.dismiss();
        this.carregandoEdicao = false;
        await this.exibirToast('Erro ao carregar veículo. Verifique o backend.');
      });
  }

  fecharEdicaoVeiculo(): void {
    this.mostrarEdicaoVeiculo = false;
    this.veiculoEditando = new Veiculo();
  }

  async salvarAlteracoesVeiculo(): Promise<void> {
    if (!this.veiculoEditando.id) {
      await this.exibirToast('Veículo inválido para atualização.');
      return;
    }

    this.salvandoEdicao = true;

    const loading = await this.controleCarregamento.create({
      message: 'Salvando alterações...',
      spinner: 'crescent',
    });

    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/veiculo/api/editar/${this.veiculoEditando.id}/`,
      data: {
        marca: this.veiculoEditando.marca,
        modelo: this.veiculoEditando.modelo,
        ano: this.veiculoEditando.ano,
        cor: this.veiculoEditando.cor,
        combustivel: this.veiculoEditando.combustivel,
      },
    };

    CapacitorHttp.patch(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 200 || resposta.status === 202) {
          await this.exibirToast('Veículo atualizado com sucesso!');
          this.fecharEdicaoVeiculo();
          await this.consultarVeiculosSistemaWeb();
        } else {
          await this.exibirToast('Nao foi possivel atualizar o veículo.');
        }

        await loading.dismiss();
        this.salvandoEdicao = false;
      })
      .catch(async (error) => {
        console.error('Erro ao atualizar veículo:', error);
        await loading.dismiss();
        this.salvandoEdicao = false;
        await this.exibirToast('Erro ao atualizar veículo. Verifique o backend.');
      });
  }

  fecharConfirmacaoExclusao(): void {
    this.mostrarConfirmacaoExclusao = false;
    this.veiculoSelecionado = null;
  }

  obterMensagemConfirmacaoExclusao(): string {
    if (!this.veiculoSelecionado) {
      return 'Deseja realmente excluir este veículo?';
    }

    return `Deseja realmente excluir ${this.veiculoSelecionado.nome_marca} ${this.veiculoSelecionado.modelo}?`;
  }

  async confirmarExclusaoVeiculo(): Promise<void> {
    if (!this.veiculoSelecionado) {
      return;
    }

    const id = this.veiculoSelecionado.id;
    this.fecharConfirmacaoExclusao();
    await this.excluirVeiculo(id);
  }

  async excluirVeiculo(id: number): Promise<void> {
    const loading = await this.controleCarregamento.create({
      message: 'Excluindo veículo...',
      spinner: 'crescent',
    });

    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/veiculo/api/deletar/${id}/`,
    };

    CapacitorHttp.delete(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 204 || resposta.status === 200) {
          await this.exibirToast('Veículo excluído com sucesso!');
          await this.consultarVeiculosSistemaWeb();
        } else {
          await this.exibirToast('Nao foi possivel excluir o veículo.');
        }

        await loading.dismiss();
      })
      .catch(async (error) => {
        console.error('Erro ao excluir veículo:', error);
        await loading.dismiss();
        await this.exibirToast('Erro ao excluir veículo. Verifique o backend.');
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
