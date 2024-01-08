# 导入模块
import img2pdf
import os
from spider_toolbox import file_tools
import PyPDF2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def pic2pdf(img_dir, out_dir, pbar):
    # print(os.path.basename(img_dir))
    # 定义pdf保存路径
    pdf_path = os.path.join(out_dir, os.path.basename(img_dir) + '.pdf')

    # 获取图片文件夹中的所有图片文件的名称
    img_files = [f for f in os.listdir(img_dir) if f.endswith(".jpg") or f.endswith(".png")]
    img_files = sorted(img_files, key=lambda x: int(x.split(".")[0]))

    # 创建一个空的pdf文件
    pdf = open(pdf_path, "wb")

    # 将图片文件夹中的所有图片转换为pdf，并写入到pdf文件中
    pdf.write(img2pdf.convert([os.path.join(img_dir, f) for f in img_files]))

    # 关闭pdf文件
    pdf.close()
    
    pbar.update()

def merge_pdfs(input_paths, output_path):
    merger = PyPDF2.PdfMerger()
    for path in input_paths:
        with open(path, 'rb') as file:
            merger.append(file)
    with open(output_path, 'wb') as output_file:
        merger.write(output_file)

def main(workdir):
    
    if input('是否转成PDF格式 (Y|n)>>>') not in ['y', 'Y', '']:
        return

    #获取漫画名
    manga_name = os.path.basename(workdir)
    #定义并创建pdf文件夹路径
    pdf_folder = os.path.join(workdir, manga_name + 'pdf')
    if not os.path.exists(pdf_folder):
        os.mkdir(pdf_folder)
    #获取所有章节的文件夹路径并以数字大小进行排序
    img_folders = [img_folder for img_folder in os.listdir(workdir) if not img_folder == manga_name + 'pdf']
    img_folders = sorted(img_folders, key=lambda x: int(x.split("_")[0]))
    img_folders = [os.path.join(workdir, img_folder) for img_folder in img_folders]
    #转为pdf
    pbar = tqdm(total=len(img_folders)+1, desc='制作PDF中...')
    thread_num = 6
    with ThreadPoolExecutor(thread_num) as f:
        for img_folder in img_folders:
            f.submit(
                pic2pdf,
                img_folder,
                pdf_folder,
                pbar
            )
    f.shutdown()
    #合并为一个pdf
    integrate_pdf = os.path.join(pdf_folder, manga_name + '.pdf')
    pdf_files = [pdf for pdf in os.listdir(pdf_folder) if not pdf == manga_name + '.pdf']
    pdf_files = sorted(pdf_files, key=lambda x: int(x.split('_')[0]))
    # print(pdf_files)
    pdf_files = [os.path.join(pdf_folder, pdf) for pdf in pdf_files]
    merge_pdfs(pdf_files, integrate_pdf)
    pbar.update()

main(r'D:\wz5222\python\Python\copymanga_downloader\Download\天狼雙星SiriusTwinStars')
