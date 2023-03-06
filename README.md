# Hướng dẫn các bước cụ thể 
Bước 1 :
       Download 2 template và Clone project về máy để chạy

      File : Frequent_less_rarely.xlsx   có 2 cột dữ liệu cần quan tâm :

      1 : Product_id (id sản phẩm)

      2 : Custom_Value (Dữ liệu mô tả tác dụng phụ của từng sản phẩm gồm các trường hợp thường gặp,ít gặp hiếm gặp) 

      File : Side_Effect.xlsx 

      1 : Id (id bênh,triệu chứng hay là biểu hiện)

      2 : Name (Tên của bệnh,triệu chứng đó)

Bước 2 : 
      Bỏ đường dẫn 2 file vừa down về vào 2 data frame tương ứng dưới đây :
    
       df_chidinh = pd.read_excel('D:/FRT/5.Python/tac_dung_phu/Frequent_less_rare/Frequent_less_rarely.xlsx')
       df_disease = pd.read_excel('D:/FRT/5.Python/tac_dung_phu/Frequent_less_rare/Side_Effect.xlsx')
       
Bước 3 :
      Nếu dữ liệu mô tả tác dụng phụ  có các thẻ dư html thì comment đoạn code này ở Funtion :
           def html_to_text_clean(filename):
      
          # remove_html_tags = BeautifulSoup(filename, 'lxml').text
          # replace_non_breaking_space = remove_html_tags.replace('\xa0', ' ')
          # remove_consecutive_space = new_trim_text(replace_non_breaking_space)
          
       Nếu không thì dữ nguyên code chạy bình thường 
       
Bước 3 :
       Xác định vị trí lưu file kết quả :
       
              df_chidinh.drop_duplicates().to_excel('D:/FRT/5.Python/Template_boc_text/ketqua_vs_v3.xlsx', index=False)
              Để đường dẫn muốn lưu file

    

