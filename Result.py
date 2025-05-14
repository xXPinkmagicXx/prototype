from Arguments import Arguments
import os

class Result:

   def __init__(self, args: Arguments, avg_response_time_ms:float, request_per_sec:float ):
      self.args = args
      self.avg_response_time = avg_response_time_ms
      self.request_per_sec = request_per_sec

   def create_new_file(self, path):
      with open(path, "w") as f:
         f.write("avg_response_time_ms")
         f.write(",")
         f.write("request_per_sec")
         f.write("\n")
      

   def is_result_valid(self) -> bool:
      if self.avg_response_time is None:
         raise ValueError(f"{self.avg_response_time}")
      if self.request_per_sec is None:
         raise ValueError(f"{self.request_per_sec}")

      return True
   
   def save_experiment_to_file(self):

      if not os.path.exists("./data/"):
         os.makedirs("./data/")

      file_name = self._get_file_name()

      directory = "./data/"
      if self.args.grpc:
         directory += "grpc/"
      elif self.args.rest:
         directory += "rest/"
      else:
         directory += "other/"
      
      if not os.path.exists(directory):
         os.makedirs(directory)

      path = directory + file_name
      if not os.path.exists(path):
         self.create_new_file(path)

      with open(path, "a") as f:
         f.write(str(self.avg_response_time))
         f.write(",")
         f.write(str(self.request_per_sec))
         f.write("\n")
      
      print(f"Saved Result to {file_name}")
   
   def _get_file_name(self):
      file_name = ""
      if self.args.secure:
         file_name += "secure"
      else:
         file_name += "insecure"

      file_name += "_" + self.args.method 
      file_name += "_" + str(self.args.n_users)
      return file_name + ".csv"
      
      
      