from Arguments import Arguments
import os

class Result:

   def __init__(self, args: Arguments, avg_response_time_ms:float, request_per_sec:float ):
      self.args = args
      self.avg_response_time = avg_response_time_ms
      self.request_per_sec = request_per_sec

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
      with open(path, "a") as f:
         f.write("avg_response_time_ms: ")
         f.write(str(self.avg_response_time))
         f.write("\n")
         f.write("request_per_sec: ")
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
      return file_name + ".txt"
      
      
      